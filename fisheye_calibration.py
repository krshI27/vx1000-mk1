import argparse
import glob
import os
from typing import List, Tuple

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calibrate an extreme fisheye lens using OpenCV's fisheye model."
    )
    parser.add_argument(
        "--images",
        required=True,
        help="Glob pattern for calibration images, e.g. 'calib/*.jpg'.",
    )
    parser.add_argument(
        "--board-width",
        type=int,
        default=9,
        help="Number of inner corners per chessboard row.",
    )
    parser.add_argument(
        "--board-height",
        type=int,
        default=6,
        help="Number of inner corners per chessboard column.",
    )
    parser.add_argument(
        "--square-size",
        type=float,
        default=1.0,
        help="Size of a chessboard square in user units (e.g. centimeters).",
    )
    parser.add_argument(
        "--output",
        default="fisheye_calibration.npz",
        help="Output file for calibration results.",
    )
    parser.add_argument(
        "--seed-d",
        type=float,
        nargs=4,
        default=[0.08, -0.16, 0.35, -0.26],
        help="Initial fisheye distortion coefficients k1 k2 k3 k4.",
    )
    parser.add_argument(
        "--fov",
        type=float,
        default=180.0,
        help="Approximate diagonal field of view for initial focal length guess.",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show undistorted preview images after calibration.",
    )
    return parser.parse_args()


def collect_calibration_points(
    images: List[np.ndarray],
    board_size: Tuple[int, int],
    square_size: float,
) -> Tuple[List[np.ndarray], List[np.ndarray], Tuple[int, int]]:
    object_points = []
    image_points = []
    pattern_size = (board_size[0], board_size[1])
    objp = np.zeros((1, board_size[0] * board_size[1], 3), np.float32)
    objp[0, :, :2] = np.mgrid[0 : board_size[0], 0 : board_size[1]].T.reshape(-1, 2)
    objp *= square_size

    valid_image_size = None

    for img in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(
            gray,
            pattern_size,
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH
            | cv2.CALIB_CB_NORMALIZE_IMAGE
            | cv2.CALIB_CB_FAST_CHECK,
        )

        if not found:
            continue

        corners = cv2.cornerSubPix(
            gray,
            corners,
            winSize=(11, 11),
            zeroZone=(-1, -1),
            criteria=(
                cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                30,
                1e-6,
            ),
        )
        image_points.append(corners)
        object_points.append(objp)

        if valid_image_size is None:
            valid_image_size = gray.shape[::-1]

    if len(image_points) < 3:
        raise RuntimeError(
            "Not enough valid calibration views were found. Check image paths and board settings."
        )

    return object_points, image_points, valid_image_size


def init_intrinsics(image_size: Tuple[int, int], fov_deg: float = 180.0) -> np.ndarray:
    width, height = image_size
    focal = 0.5 * width / np.tan(np.deg2rad(fov_deg) / 2.0)
    K = np.array(
        [[focal, 0.0, width / 2.0], [0.0, focal, height / 2.0], [0.0, 0.0, 1.0]],
        dtype=np.float64,
    )
    return K


def calibrate_fisheye(
    object_points: List[np.ndarray],
    image_points: List[np.ndarray],
    image_size: Tuple[int, int],
    seed_d: List[float],
    fov: float,
) -> Tuple[np.ndarray, np.ndarray, float]:
    K = init_intrinsics(image_size, fov_deg=fov)
    D = np.array(seed_d, dtype=np.float64).reshape(4, 1)

    flags = (
        cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC
        | cv2.fisheye.CALIB_CHECK_COND
        | cv2.fisheye.CALIB_FIX_SKEW
    )

    rms, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
        object_points,
        image_points,
        image_size,
        K,
        D,
        flags=flags,
        criteria=(
            cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
            100,
            1e-6,
        ),
    )

    return K, D, rms


def undistort_image(
    image: np.ndarray,
    K: np.ndarray,
    D: np.ndarray,
    balance: float = 0.0,
) -> np.ndarray:
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(
        K,
        D,
        np.eye(3, dtype=np.float64),
        K,
        image.shape[1::-1],
        cv2.CV_16SC2,
    )
    return cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR)


def save_calibration(
    output_path: str, K: np.ndarray, D: np.ndarray, image_size: Tuple[int, int]
) -> None:
    np.savez(output_path, K=K, D=D, image_size=np.array(image_size, dtype=np.int32))
    print(f"Calibration saved to {output_path}")


def main() -> None:
    args = parse_args()
    image_paths = sorted(glob.glob(args.images))

    if not image_paths:
        raise FileNotFoundError(f"No images found for pattern: {args.images}")

    images = [cv2.imread(path) for path in image_paths]
    object_points, image_points, image_size = collect_calibration_points(
        images,
        board_size=(args.board_width, args.board_height),
        square_size=args.square_size,
    )

    K, D, rms = calibrate_fisheye(
        object_points,
        image_points,
        image_size,
        seed_d=args.seed_d,
        fov=args.fov,
    )

    print("Fisheye calibration complete")
    print(f"RMS reprojection error: {rms:.6f}")
    print("Intrinsic matrix K:")
    print(K)
    print("Distortion coefficients D:")
    print(D.ravel())

    save_calibration(args.output, K, D, image_size)

    if args.show:
        for path, image in zip(image_paths, images):
            undistorted = undistort_image(image, K, D)
            combined = np.hstack((image, undistorted))
            cv2.imshow("Original | Undistorted", combined)
            cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
