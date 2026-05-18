import math
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring

from otio_svg_adapter.primitives import (
    COLORS,
    Point,
    convert_point_to_svg_coordinates,
    convert_rect_to_svg_coordinates,
)


class SVGWriter:
    def __init__(
        self,
        image_width=2406.0,
        image_height=1054.0,
        image_margin=20.0,
        arrow_margin=10.0,
        arrow_label_margin=5.0,
        font_size=15.0,
        font_family="sans-serif",
    ):
        self.image_width = image_width
        self.image_height = image_height
        self.image_margin = image_margin
        self.arrow_margin = arrow_margin
        self.arrow_label_margin = arrow_label_margin
        self.font_size = font_size
        self.text_margin = 0.5 * font_size
        self.font_family = font_family

        self.all_clips_data = []
        self.trackwise_clip_count = []
        self.tracks_duration = []
        self.track_transition_available = []
        self.max_total_duration = 0
        self.global_min_time = 0
        self.global_max_time = 0
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.x_origin = 0
        self.clip_rect_height = 0
        self.vertical_drawing_index = -1
        self.svg_elem = Element(
            "svg",
            {
                "height": f"{self.image_height:.8f}",
                "width": f"{self.image_width:.8f}",
                "version": "4.0",
                "xmlns": "http://www.w3.org/2000/svg",
                "xmlns:xlink": "http://www.w3.org/1999/xlink",
            },
        )

        # white background
        SubElement(
            self.svg_elem,
            "rect",
            {
                "width": "100%",
                "height": "100%",
                "fill": "white",
            },
        )

    def draw_rect(self, rect, stroke_width=2.0, stroke_color=COLORS["black"]):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        SubElement(
            self.svg_elem,
            "rect",
            {
                "x": f"{svg_rect.origin.x:.8f}",
                "y": f"{svg_rect.origin.y:.8f}",
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "style": "fill:rgb(255,255,255);stroke-width:{:.8f};"
                "stroke:{};opacity:1;fill-opacity:0;".format(
                    stroke_width, stroke_color.svg_color()
                ),
            },
        )

    def draw_labeled_rect(
        self,
        rect,
        stroke_width=2.0,
        stroke_color=COLORS["black"],
        fill_color=COLORS["white"],
        label="",
        label_size=10.0,
    ):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        g_elem = SubElement(
            self.svg_elem,
            "g",
            {
                "transform": "translate({:.8f},{:.8f})".format(
                    svg_rect.origin.x, svg_rect.origin.y
                )
            },
        )
        SubElement(
            g_elem,
            "rect",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "style": "fill:{};stroke-width:{:.8f};stroke:{};opacity:1;".format(
                    fill_color.svg_color(),
                    stroke_width,
                    stroke_color.svg_color(),
                ),
            },
        )
        sub_svg_elem = SubElement(
            g_elem,
            "svg",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
            },
        )
        text_elem = SubElement(
            sub_svg_elem,
            "text",
            {
                "x": "50%",
                "y": "50%",
                "font-size": f"{label_size:.8f}",
                "font-family": self.font_family,
                "style": "stroke:{};stroke-width:{:.8f};fill:{};opacity:{:.8f};".format(
                    COLORS["black"].svg_color(),
                    stroke_width / 4.0,
                    COLORS["black"].svg_color(),
                    COLORS["black"].a,
                ),
                "alignment-baseline": "middle",
                "text-anchor": "middle",
            },
        )
        text_elem.text = label

    def draw_dashed_rect(
        self,
        rect,
        stroke_width=2.0,
        stroke_color=COLORS["black"],
        fill_color=COLORS["white"],
    ):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        SubElement(
            self.svg_elem,
            "rect",
            {
                "x": f"{svg_rect.origin.x:.8f}",
                "y": f"{svg_rect.origin.y:.8f}",
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "stroke-dasharray": "5",
                "style": "fill:{};stroke-width:{:.8f};stroke:{};"
                "opacity:1;fill-opacity:{:.8f}".format(
                    fill_color.svg_color(),
                    stroke_width,
                    stroke_color.svg_color(),
                    fill_color.a,
                ),
            },
        )

    def draw_labeled_dashed_rect_with_border(
        self,
        rect,
        stroke_width=2.0,
        fill_color=COLORS["white"],
        border_color=COLORS["black"],
        label="",
        label_size=10.0,
    ):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        g_elem = SubElement(
            self.svg_elem,
            "g",
            {
                "transform": "translate({:.8f},{:.8f})".format(
                    svg_rect.origin.x, svg_rect.origin.y
                )
            },
        )
        SubElement(
            g_elem,
            "rect",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "stroke-dasharray": "5",
                "style": "fill:{};stroke-width:{:.8f};stroke:{};opacity:{:.8f};".format(
                    fill_color.svg_color(),
                    stroke_width,
                    border_color.svg_color(),
                    fill_color.a,
                ),
            },
        )
        sub_svg_elem = SubElement(
            g_elem,
            "svg",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
            },
        )
        text_elem = SubElement(
            sub_svg_elem,
            "text",
            {
                "x": "50%",
                "y": "50%",
                "font-size": f"{label_size:.8f}",
                "font-family": self.font_family,
                "style": "stroke:{};stroke-width:{:.8f};fill:{};opacity:{:.8f};".format(
                    COLORS["black"].svg_color(),
                    stroke_width / 4.0,
                    COLORS["black"].svg_color(),
                    COLORS["black"].a,
                ),
                "alignment-baseline": "middle",
                "text-anchor": "middle",
            },
        )
        text_elem.text = label

    def draw_solid_rect(self, rect, fill_color=COLORS["white"]):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        SubElement(
            self.svg_elem,
            "rect",
            {
                "x": f"{svg_rect.origin.x:.8f}",
                "y": f"{svg_rect.origin.y:.8f}",
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "style": "fill:{};stroke-width:0;"
                "stroke:rgb(0,0,0);opacity:{:.8f};".format(
                    fill_color.svg_color(), fill_color.a
                ),
            },
        )

    def draw_solid_rect_with_border(
        self,
        rect,
        stroke_width=2.0,
        fill_color=COLORS["white"],
        border_color=COLORS["black"],
    ):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        SubElement(
            self.svg_elem,
            "rect",
            {
                "x": f"{svg_rect.origin.x:.8f}",
                "y": f"{svg_rect.origin.y:.8f}",
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "style": "fill:{};stroke-width:{:.8f};stroke:{};opacity:{:.8f};".format(
                    fill_color.svg_color(),
                    stroke_width,
                    border_color.svg_color(),
                    fill_color.a,
                ),
            },
        )

    def draw_labeled_solid_rect_with_border(
        self,
        rect,
        stroke_width=2.0,
        fill_color=COLORS["white"],
        border_color=COLORS["black"],
        label="",
        label_size=10.0,
    ):
        svg_rect = convert_rect_to_svg_coordinates(rect, self.image_height)
        g_elem = SubElement(
            self.svg_elem,
            "g",
            {
                "transform": "translate({:.8f},{:.8f})".format(
                    svg_rect.origin.x, svg_rect.origin.y
                )
            },
        )
        SubElement(
            g_elem,
            "rect",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
                "style": "fill:{};stroke-width:{:.8f};stroke:{};opacity:{:.8f};".format(
                    fill_color.svg_color(),
                    stroke_width,
                    border_color.svg_color(),
                    fill_color.a,
                ),
            },
        )
        sub_svg_elem = SubElement(
            g_elem,
            "svg",
            {
                "width": f"{svg_rect.width:.8f}",
                "height": f"{svg_rect.height:.8f}",
            },
        )
        text_elem = SubElement(
            sub_svg_elem,
            "text",
            {
                "x": "50%",
                "y": "50%",
                "font-size": f"{label_size:.8f}",
                "font-family": self.font_family,
                "style": "stroke:{};stroke-width:{:.8f};fill:{};opacity:{:.8f};".format(
                    COLORS["black"].svg_color(),
                    stroke_width / 4.0,
                    COLORS["black"].svg_color(),
                    COLORS["black"].a,
                ),
                "alignment-baseline": "middle",
                "text-anchor": "middle",
            },
        )
        text_elem.text = label

    def draw_line(
        self,
        start_point,
        end_point,
        stroke_width,
        stroke_color=COLORS["black"],
        is_dashed=False,
    ):
        point1 = convert_point_to_svg_coordinates(
            start_point, self.image_height
        )
        point2 = convert_point_to_svg_coordinates(end_point, self.image_height)
        style_str = "stroke-width:{:.8f};stroke:{};opacity:{:.8f};stroke-linecap:butt;".format(
            stroke_width, stroke_color.svg_color(), stroke_color.a
        )
        if is_dashed:
            style_str = style_str + "stroke-dasharray:4 1"
        SubElement(
            self.svg_elem,
            "line",
            {
                "x1": f"{point1.x:.8f}",
                "y1": f"{point1.y:.8f}",
                "x2": f"{point2.x:.8f}",
                "y2": f"{point2.y:.8f}",
                "style": style_str,
            },
        )

    def draw_arrow(
        self,
        start_point,
        end_point,
        stroke_width,
        stroke_color=COLORS["black"],
    ):
        point1 = convert_point_to_svg_coordinates(
            start_point, self.image_height
        )
        point2 = convert_point_to_svg_coordinates(end_point, self.image_height)
        direction = Point(point2.x - point1.x, point2.y - point1.y)
        direction_magnitude = math.sqrt(
            direction.x * direction.x + direction.y * direction.y
        )
        inv_magnitude = 1.0 / direction_magnitude
        arrowhead_length = 9.0
        arrowhead_half_width = arrowhead_length * 0.5
        direction = Point(
            direction.x * inv_magnitude, direction.y * inv_magnitude
        )
        point2 = Point(
            point2.x - arrowhead_length * direction.x,
            point2.y - arrowhead_length * direction.y,
        )
        triangle_tip = Point(
            point2.x + arrowhead_length * direction.x,
            point2.y + arrowhead_length * direction.y,
        )
        perpendicular_dir = Point(-direction.y, direction.x)
        triangle_pt_1 = Point(
            point2.x + arrowhead_half_width * perpendicular_dir.x,
            point2.y + arrowhead_half_width * perpendicular_dir.y,
        )
        triangle_pt_2 = Point(
            point2.x - arrowhead_half_width * perpendicular_dir.x,
            point2.y - arrowhead_half_width * perpendicular_dir.y,
        )
        SubElement(
            self.svg_elem,
            "line",
            {
                "x1": f"{point1.x:.8f}",
                "y1": f"{point1.y:.8f}",
                "x2": f"{point2.x:.8f}",
                "y2": f"{point2.y:.8f}",
                "style": "stroke-width:{:.8f};stroke:{};opacity:{:.8f};"
                "stroke-linecap:butt;".format(
                    stroke_width, stroke_color.svg_color(), stroke_color.a
                ),
            },
        )
        SubElement(
            self.svg_elem,
            "polygon",
            {
                "points": " ".join(
                    p.svg_point_string()
                    for p in [triangle_tip, triangle_pt_1, triangle_pt_2]
                ),
                "style": f"fill:{stroke_color.svg_color()};",
            },
        )

    def draw_text(
        self,
        text,
        location,
        text_size,
        color=COLORS["black"],
        stroke_width=1.0,
    ):
        location_svg = convert_point_to_svg_coordinates(
            location, self.image_height
        )
        text_elem = SubElement(
            self.svg_elem,
            "text",
            {
                "x": f"{location_svg.x:.8f}",
                "y": f"{location_svg.y:.8f}",
                "font-size": f"{text_size:.8f}",
                "font-family": self.font_family,
                "style": "stroke:{};stroke-width:{:.8f};fill:{};opacity:{:.8f};".format(
                    color.svg_color(),
                    stroke_width / 4.0,
                    color.svg_color(),
                    color.a,
                ),
            },
        )
        text_elem.text = text

    def get_image(self):
        xmlstr = tostring(
            self.svg_elem, encoding="utf-8", method="xml"
        ).decode("utf8")

        return minidom.parseString(xmlstr).toprettyxml(indent="  ")
