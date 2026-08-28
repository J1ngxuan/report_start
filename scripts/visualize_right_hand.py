#!/usr/bin/env python3
"""Visualize the moving right end-effector in a VR teleoperation episode.

The HDF5 file does not contain field-name metadata for ``robot_pose``.  This
script therefore uses the layout inferred from the data:

    [left_x, left_y, left_z, left_roll, left_pitch, left_yaw, left_gripper,
     right_x, right_y, right_z, right_roll, right_pitch, right_yaw,
     right_gripper]

RPY angles are interpreted in radians with R = Rz(yaw) Ry(pitch) Rx(roll).
The orientation arrow shows the tool-frame +Z axis.  For this PCBA placement
task, gripper state 1 means holding and state 0 means released.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable

import h5py
import numpy as np
from PIL import Image, ImageDraw, ImageFont


REGULAR_FONT_CANDIDATES = (
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
    "/usr/local/share/fonts/simsun.ttc",
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-regular.otf",
)
BOLD_FONT_CANDIDATES = (
    "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-bold.otf",
)
LATIN_FONT_CANDIDATES = (
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-regular.otf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf",
)
LATIN_ITALIC_FONT_CANDIDATES = (
    "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyretermes-italic.otf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Italic.ttf",
)

COLORS = {
    0: (0, 86, 179),     # academic blue
    1: (210, 45, 42),    # academic red
}
INK = (20, 20, 20)
MUTED = (78, 78, 78)
GRID = (196, 196, 196)
LIGHT_GRID = (222, 222, 222)
WHITE = (255, 255, 255)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = BOLD_FONT_CANDIDATES if bold else REGULAR_FONT_CANDIDATES
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def load_latin_font(size: int, italic: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = LATIN_ITALIC_FONT_CANDIDATES if italic else LATIN_FONT_CANDIDATES
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def state_color(value: float) -> tuple[int, int, int]:
    """Map binary gripper values to two colorblind-friendly colors."""
    return COLORS[int(value >= 0.5)]


def rpy_to_direction(rpy: np.ndarray) -> np.ndarray:
    """Return the world direction of tool-frame +Z for roll-pitch-yaw."""
    roll, pitch, yaw = (float(v) for v in rpy)
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    rotation = np.array(
        [
            [cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr],
            [sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr],
            [-sp, cp * sr, cp * cr],
        ],
        dtype=float,
    )
    return rotation[:, 2]


def chw_to_pil(frame: np.ndarray) -> Image.Image:
    if frame.ndim != 3:
        raise ValueError(f"Expected a three-dimensional image, got {frame.shape}")
    if frame.shape[0] in (1, 3, 4):
        frame = np.moveaxis(frame, 0, -1)
    if frame.shape[-1] == 1:
        frame = frame[..., 0]
    return Image.fromarray(np.asarray(frame, dtype=np.uint8))


class Projector:
    """Equal-scale orthographic projection from XYZ to an image rectangle."""

    def __init__(
        self,
        bounds: np.ndarray,
        canvas_size: tuple[int, int],
        margins: tuple[int, int, int, int],
        azimuth_deg: float = 43.0,
        elevation_deg: float = 25.0,
    ) -> None:
        self.bounds = np.asarray(bounds, dtype=float)
        self.center = self.bounds.mean(axis=1)
        azimuth = math.radians(azimuth_deg)
        elevation = math.radians(elevation_deg)
        self.screen_right = np.array([-math.sin(azimuth), math.cos(azimuth), 0.0])
        self.screen_up = np.array(
            [
                -math.sin(elevation) * math.cos(azimuth),
                -math.sin(elevation) * math.sin(azimuth),
                math.cos(elevation),
            ]
        )
        width, height = canvas_size
        left, top, right, bottom = margins
        corners = np.array(
            [
                [x, y, z]
                for x in self.bounds[0]
                for y in self.bounds[1]
                for z in self.bounds[2]
            ],
            dtype=float,
        )
        raw = self._raw(corners)
        raw_min = raw.min(axis=0)
        raw_max = raw.max(axis=0)
        usable_w = width - left - right
        usable_h = height - top - bottom
        raw_span = np.maximum(raw_max - raw_min, 1e-9)
        self.scale = min(usable_w / raw_span[0], usable_h / raw_span[1])
        drawn_w, drawn_h = raw_span * self.scale
        self.offset = np.array(
            [left + (usable_w - drawn_w) / 2, top + (usable_h - drawn_h) / 2]
        ) - raw_min * self.scale

    def _raw(self, points: np.ndarray) -> np.ndarray:
        centered = np.atleast_2d(points) - self.center
        return np.column_stack(
            (centered @ self.screen_right, -(centered @ self.screen_up))
        )

    def __call__(self, points: np.ndarray) -> np.ndarray:
        return self._raw(points) * self.scale + self.offset


def draw_polyline(
    draw: ImageDraw.ImageDraw,
    points: np.ndarray,
    fill: tuple[int, int, int],
    width: int,
) -> None:
    draw.line([tuple(v) for v in points], fill=fill, width=width, joint="curve")


def draw_dashed_polyline(
    draw: ImageDraw.ImageDraw,
    points: np.ndarray,
    fill: tuple[int, int, int],
    width: int,
    dash: float = 22.0,
    gap: float = 14.0,
) -> None:
    """Draw a dash pattern continuously along a projected polyline."""
    points = np.asarray(points, dtype=float)
    if len(points) < 2:
        return
    period = dash + gap
    distance_on_pattern = 0.0
    for start, end in zip(points[:-1], points[1:]):
        vector = end - start
        segment_length = float(np.linalg.norm(vector))
        if segment_length < 1e-9:
            continue
        unit = vector / segment_length
        cursor = 0.0
        while cursor < segment_length:
            phase = distance_on_pattern % period
            drawing = phase < dash
            remaining = (dash - phase) if drawing else (period - phase)
            step = min(remaining, segment_length - cursor)
            if drawing and step > 0:
                p0 = start + unit * cursor
                p1 = start + unit * (cursor + step)
                draw.line([tuple(p0), tuple(p1)], fill=fill, width=width)
            cursor += step
            distance_on_pattern += step


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: np.ndarray,
    end: np.ndarray,
    color: tuple[int, int, int],
    width: int = 5,
    head_length: float = 15.0,
    halo: bool = True,
) -> None:
    start = np.asarray(start, dtype=float)
    end = np.asarray(end, dtype=float)
    vector = end - start
    length = float(np.linalg.norm(vector))
    if length < 1e-6:
        return
    unit = vector / length
    perpendicular = np.array([-unit[1], unit[0]])
    base = end - unit * min(head_length, length * 0.45)
    left = base + perpendicular * head_length * 0.46
    right = base - perpendicular * head_length * 0.46
    if halo:
        draw.line([tuple(start), tuple(end)], fill=WHITE, width=width + 5)
        draw.polygon([tuple(end), tuple(left), tuple(right)], fill=WHITE)
    draw.line([tuple(start), tuple(end)], fill=color, width=width)
    draw.polygon([tuple(end), tuple(left), tuple(right)], fill=color)


def draw_axis_ticks(
    draw: ImageDraw.ImageDraw,
    projector: Projector,
    origin: np.ndarray,
    axis: int,
    bounds: np.ndarray,
    axis_label: str,
    font: ImageFont.ImageFont,
    label_font: ImageFont.ImageFont,
) -> None:
    start = origin.copy()
    end = origin.copy()
    end[axis] = bounds[axis, 1]
    p0, p1 = projector(np.vstack((start, end)))
    draw_arrow(draw, p0, p1, INK, width=4, head_length=14, halo=False)

    axis_vector = p1 - p0
    axis_unit = axis_vector / max(np.linalg.norm(axis_vector), 1e-9)
    tick_normal = np.array([-axis_unit[1], axis_unit[0]])
    if tick_normal[1] < 0:
        tick_normal *= -1
    tick_values = np.linspace(bounds[axis, 0], bounds[axis, 1], 5)
    for tick_index, value in enumerate(tick_values):
        point = origin.copy()
        point[axis] = value
        p = projector(point)[0]
        draw.line(
            [tuple(p - tick_normal * 6), tuple(p + tick_normal * 6)],
            fill=INK,
            width=2,
        )
        # The three minimum values share one projected origin and would overlap.
        if tick_index > 0:
            label = f"{value:.2f}"
            box = draw.textbbox((0, 0), label, font=font)
            text_w = box[2] - box[0]
            pos = p + tick_normal * 13 - np.array([text_w / 2, 0])
            draw.text(tuple(pos), label, font=font, fill=MUTED)

    label_pos = p1 + axis_unit * 72 + tick_normal * 12
    draw.text(tuple(label_pos), axis_label, font=label_font, fill=INK, anchor="mm")


def render_trajectory(
    position: np.ndarray,
    rpy: np.ndarray,
    gripper: np.ndarray,
    selected: list[int],
    output_path: Path,
) -> Image.Image:
    width, height = 2400, 1600
    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    axis_font = load_latin_font(34)
    axis_label_font = load_latin_font(50, italic=True)
    legend_font = load_font(60)
    annotation_font = load_font(46)
    note_font = load_font(34)

    mins = position.min(axis=0)
    maxs = position.max(axis=0)
    span = np.maximum(maxs - mins, 1e-3)
    padding = np.maximum(span * 0.10, 0.006)
    bounds = np.column_stack((mins - padding, maxs + padding))
    projector = Projector(
        bounds,
        (width, height),
        (315, 105, 270, 245),
        azimuth_deg=40.0,
        elevation_deg=24.0,
    )

    # Thin, neutral 3-D grid matching conventional scientific plotting.
    for x in np.linspace(bounds[0, 0], bounds[0, 1], 7):
        points = np.array(
            [[x, bounds[1, 0], bounds[2, 0]], [x, bounds[1, 1], bounds[2, 0]]]
        )
        draw_polyline(draw, projector(points), LIGHT_GRID, 1)
    for y in np.linspace(bounds[1, 0], bounds[1, 1], 7):
        points = np.array(
            [[bounds[0, 0], y, bounds[2, 0]], [bounds[0, 1], y, bounds[2, 0]]]
        )
        draw_polyline(draw, projector(points), LIGHT_GRID, 1)

    for z in np.linspace(bounds[2, 0], bounds[2, 1], 6):
        for fixed_x in (bounds[0, 0], bounds[0, 1]):
            points = np.array(
                [[fixed_x, bounds[1, 0], z], [fixed_x, bounds[1, 1], z]]
            )
            draw_polyline(draw, projector(points), LIGHT_GRID, 1)

    # Bounding-box edges provide depth cues.
    corners = {
        (ix, iy, iz): np.array([bounds[0, ix], bounds[1, iy], bounds[2, iz]])
        for ix in (0, 1)
        for iy in (0, 1)
        for iz in (0, 1)
    }
    for key, point in corners.items():
        for axis in range(3):
            if key[axis] != 0:
                continue
            other_key = list(key)
            other_key[axis] = 1
            other = corners[tuple(other_key)]
            draw_polyline(draw, projector(np.vstack((point, other))), GRID, 1)

    # Draw contiguous path runs.  Color and line style both encode gripper state.
    projected_path = projector(position)
    binary_state = (gripper >= 0.5).astype(int)
    run_starts = [0] + (np.flatnonzero(np.diff(binary_state) != 0) + 1).tolist()
    run_ends = run_starts[1:] + [len(position)]
    for start, end in zip(run_starts, run_ends):
        run_points = projected_path[start:end]
        state = int(binary_state[start])
        if len(run_points) == 1 and start > 0:
            run_points = projected_path[start - 1 : end]
        elif start > 0:
            run_points = projected_path[start - 1 : end]
        if state == 0:
            draw_polyline(draw, run_points, COLORS[state], 6)
        else:
            draw_dashed_polyline(draw, run_points, COLORS[state], 6, dash=25, gap=15)

    # Sparse black arrows preserve orientation information without dominating.
    sampled = set(np.linspace(0, len(position) - 1, 9).round().astype(int).tolist())
    arrow_length_m = 0.020
    for i in sorted(sampled):
        direction = rpy_to_direction(rpy[i])
        arrow_3d = np.vstack((position[i], position[i] + direction * arrow_length_m))
        arrow_2d = projector(arrow_3d)
        draw_arrow(draw, arrow_2d[0], arrow_2d[1], INK, width=3, head_length=11, halo=False)

    # Conventional start/end markers and a single open marker for the middle frame.
    start_p = projected_path[0]
    end_p = projected_path[-1]
    mid_p = projected_path[selected[1]]
    marker_radius = 11
    draw.ellipse(
        (
            start_p[0] - marker_radius,
            start_p[1] - marker_radius,
            start_p[0] + marker_radius,
            start_p[1] + marker_radius,
        ),
        fill=INK,
    )
    draw.rectangle(
        (
            end_p[0] - marker_radius,
            end_p[1] - marker_radius,
            end_p[0] + marker_radius,
            end_p[1] + marker_radius,
        ),
        fill=INK,
    )
    draw.ellipse(
        (
            mid_p[0] - marker_radius,
            mid_p[1] - marker_radius,
            mid_p[0] + marker_radius,
            mid_p[1] + marker_radius,
        ),
        fill=WHITE,
        outline=INK,
        width=3,
    )
    draw.text((start_p[0] + 24, start_p[1] + 10), "起点", font=annotation_font, fill=INK)
    draw.text((end_p[0] + 24, end_p[1] + 30), "终点", font=annotation_font, fill=INK)
    draw.text(
        (mid_p[0] + 18, mid_p[1] - 34),
        f"第 {selected[1]} 帧",
        font=annotation_font,
        fill=INK,
    )

    origin = np.array([bounds[0, 0], bounds[1, 0], bounds[2, 0]], dtype=float)
    draw_axis_ticks(draw, projector, origin, 0, bounds, "X (m)", axis_font, axis_label_font)
    draw_axis_ticks(draw, projector, origin, 1, bounds, "Y (m)", axis_font, axis_label_font)
    draw_axis_ticks(draw, projector, origin, 2, bounds, "Z (m)", axis_font, axis_label_font)

    # Compact boxed legend, as used in conventional journal figures.
    legend_box = (105, 75, 750, 450)
    draw.rectangle(legend_box, fill=WHITE, outline=INK, width=2)
    legend_entries = [
        ("state0", "夹爪松开（0）"),
        ("state1", "夹爪夹持（1）"),
        ("arrow", "末端朝向"),
        ("start", "轨迹起点"),
        ("end", "轨迹终点"),
    ]
    for row, (kind, label) in enumerate(legend_entries):
        y = 125 + row * 69
        x0, x1 = 145, 255
        if kind == "state0":
            draw.line((x0, y, x1, y), fill=COLORS[0], width=6)
        elif kind == "state1":
            draw_dashed_polyline(
                draw,
                np.array([[x0, y], [x1, y]], dtype=float),
                COLORS[1],
                6,
                dash=20,
                gap=12,
            )
        elif kind == "arrow":
            draw_arrow(
                draw,
                np.array([x0, y], dtype=float),
                np.array([x1, y], dtype=float),
                INK,
                width=3,
                head_length=11,
                halo=False,
            )
        elif kind == "start":
            draw.ellipse((190, y - 12, 214, y + 12), fill=INK)
        else:
            draw.rectangle((190, y - 12, 214, y + 12), fill=INK)
        draw.text((295, y), label, font=legend_font, fill=INK, anchor="lm")

    draw.text(
        (width - 95, height - 42),
        f"轨迹点数 N = {len(position)}，轨迹长度 = {np.linalg.norm(np.diff(position, axis=0), axis=1).sum():.3f} m",
        font=note_font,
        fill=MUTED,
        anchor="rs",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, dpi=(300, 300), optimize=True)
    return image


def add_snapshot_panel(
    canvas: Image.Image,
    frame: Image.Image,
    x: int,
    y: int,
    panel_w: int,
    number: int,
    frame_index: int,
    progress: float,
    gripper: float,
) -> None:
    draw = ImageDraw.Draw(canvas)
    caption_font = load_font(60)
    ratio = panel_w / frame.width
    resized = frame.resize((panel_w, round(frame.height * ratio)), Image.Resampling.LANCZOS)
    canvas.paste(resized, (x, y))
    draw.rectangle((x, y, x + resized.width - 1, y + resized.height - 1), outline=INK, width=2)
    caption_y = y + resized.height + 24
    stage = ("起始时刻", "中间时刻", "结束时刻")[number - 1]
    gripper_text = "夹持" if gripper >= 0.5 else "松开"
    label = (
        f"({chr(96 + number)}) {stage}（第 {frame_index} 帧）\n"
        f"进度 {progress:.0%}，夹爪{gripper_text}"
    )
    draw.multiline_text(
        (x + panel_w / 2, caption_y),
        label,
        font=caption_font,
        fill=INK,
        anchor="ma",
        align="center",
        spacing=8,
    )


def render_overview(
    frames: list[Image.Image],
    selected: list[int],
    progress: np.ndarray,
    gripper: np.ndarray,
    trajectory: Image.Image,
    output_path: Path,
) -> None:
    width, height = 2400, 2220
    canvas = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(canvas)
    panel_label_font = load_font(60)

    panel_w = 700
    gap = 50
    start_x = (width - (3 * panel_w + 2 * gap)) // 2
    for j, (frame, frame_index) in enumerate(zip(frames, selected)):
        add_snapshot_panel(
            canvas,
            frame,
            start_x + j * (panel_w + gap),
            70,
            panel_w,
            j + 1,
            frame_index,
            float(progress[frame_index]),
            float(gripper[frame_index]),
        )

    # The trajectory is the dominant panel, with a conventional subfigure label.
    trajectory_copy = trajectory.copy()
    trajectory_copy.thumbnail((2200, 1320), Image.Resampling.LANCZOS)
    tx = (width - trajectory_copy.width) // 2
    ty = 770
    canvas.paste(trajectory_copy, (tx, ty))
    draw.text(
        (width / 2, height - 58),
        "(d) 右手末端执行器三维轨迹",
        font=panel_label_font,
        fill=INK,
        anchor="ms",
    )
    canvas.save(output_path, dpi=(300, 300), optimize=True)


def parse_frame_list(value: str | None, count: int) -> list[int]:
    if value is None:
        return [0, count // 2, count - 1]
    frames = [int(part.strip()) for part in value.split(",") if part.strip()]
    if len(frames) != 3:
        raise ValueError("--frames must contain exactly three comma-separated indices")
    if min(frames) < 0 or max(frames) >= count:
        raise ValueError(f"Frame indices must be in [0, {count - 1}]")
    return frames


def validate_datasets(handle: h5py.File) -> None:
    required = ("right_arm_image", "robot_pose", "progress")
    missing = [name for name in required if name not in handle]
    if missing:
        raise KeyError(f"Missing HDF5 datasets: {', '.join(missing)}")
    if handle["robot_pose"].ndim != 2 or handle["robot_pose"].shape[1] < 14:
        raise ValueError("robot_pose must have shape [frames, >=14]")


def write_summary(
    path: Path,
    input_path: Path,
    selected: Iterable[int],
    progress: np.ndarray,
    position: np.ndarray,
    gripper: np.ndarray,
) -> None:
    selected = list(selected)
    states, counts = np.unique((gripper >= 0.5).astype(int), return_counts=True)
    state_counts = {int(state): int(count) for state, count in zip(states, counts)}
    transitions = (np.flatnonzero(np.diff((gripper >= 0.5).astype(int)) != 0) + 1).tolist()
    path_length = float(np.linalg.norm(np.diff(position, axis=0), axis=1).sum())
    lines = [
        "# 右手可视化数据摘要",
        "",
        f"- 数据文件：`{input_path}`",
        f"- 总帧数：{len(position)}",
        f"- 截图帧：{', '.join(str(i) for i in selected)}",
        f"- 截图进度：{', '.join(f'{progress[i]:.1%}' for i in selected)}",
        f"- 右手轨迹长度：{path_length:.6f} m",
        f"- 夹爪状态计数：{state_counts}",
        f"- 夹爪状态切换帧：{transitions or '无'}",
        "",
        "## 位姿解释",
        "",
        "`robot_pose` 按左右手各 7 维解析：`[x, y, z, roll, pitch, yaw, gripper]`。",
        "方向箭头使用 `Rz(yaw) @ Ry(pitch) @ Rx(roll)` 作用后的工具坐标系 `+Z` 轴。",
        "在该PCBA放置任务中，夹爪状态1表示夹持，状态0表示松开。",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Input HDF5 episode")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("figures/right_hand_visualization"),
        help="Directory for PNG outputs",
    )
    parser.add_argument(
        "--frames",
        help="Exactly three comma-separated frame indices; default: start,middle,end",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with h5py.File(args.input, "r") as handle:
        validate_datasets(handle)
        pose = np.asarray(handle["robot_pose"], dtype=float)
        progress = np.asarray(handle["progress"][:, 0], dtype=float)
        selected = parse_frame_list(args.frames, len(pose))
        frames = [chw_to_pil(handle["right_arm_image"][i]) for i in selected]

    right = pose[:, 7:14]
    position = right[:, :3]
    rpy = right[:, 3:6]
    gripper = right[:, 6]

    for frame, index in zip(frames, selected):
        frame.save(args.output_dir / f"right_arm_frame_{index:03d}.png", optimize=True)

    trajectory_path = args.output_dir / "right_hand_trajectory.png"
    trajectory = render_trajectory(position, rpy, gripper, selected, trajectory_path)
    render_overview(
        frames,
        selected,
        progress,
        gripper,
        trajectory,
        args.output_dir / "right_hand_overview.png",
    )
    write_summary(
        args.output_dir / "README.md",
        args.input.resolve(),
        selected,
        progress,
        position,
        gripper,
    )

    print(f"Saved three snapshots and trajectory figures to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
