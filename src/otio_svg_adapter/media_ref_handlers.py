from typing import Any, Protocol

import opentimelineio as otio

from otio_svg_adapter.primitives import Point
from otio_svg_adapter.writer import SVGWriter


class MediaReferenceInfoHandler(Protocol):
    """
    Handler responsible for drawing media reference info.

    The implementations draw media-specific info through the provided SVG Writer
    in relation to a specific origin `Point`.

    The basic components that this handler might draw include:
        - available range
        - target url

    Info items can be added/omitted based on the specific media reference type.
    """

    @staticmethod
    def draw_info(
        clip: otio.schema.Clip, svg_writer: SVGWriter, media_origin: Point
    ):
        """
        Draw the info components for a given clip
        """
        ...


_handler_registry: dict[Any, MediaReferenceInfoHandler] = {}


def draw_media_reference_info(
    clip: otio.schema.Clip, svg_writer: SVGWriter, origin: Point
):
    """
    Draws the media reference info components based on the reference
    type included in the `Clip`
    """
    handler = _handler_registry.get(
        type(clip.media_reference), DefaultMediaReferenceHandler
    )
    handler.draw_info(clip=clip, svg_writer=svg_writer, media_origin=origin)


def register_handler(otio_type):
    """
    Registers an otio type provided with a class implementing the
    `MediaReferenceInfoHandler` protocol using a decorator


    Example:
        ```
        import opentimelineio as otio

        @register_handler(otio.schema.LongFormMediaReference)
        class LongMediaReferenceHandler(MediaReferenceInfoHandler):
            @classmethod
            def handle(...):
                ...
        ```
    """

    def decorator(cls):
        _handler_registry[otio_type] = cls
        return cls

    return decorator


@register_handler(otio.schema.ImageSequenceReference)
class ImageSequenceReferenceHandler(MediaReferenceInfoHandler):
    """
    Draws the `ImageSequenceReference` info with the SVG Writer,
    including the following components:
        - available range
        - target url (ranged)

    Since this type of reference contains a collection of frames with
    a start, step, and a base url, the final drawn url follows the
    standard linux `{START..END[..INCREMENT]}` formatting.

    The final result also takes into account the total zero padding
    for the frame number, and the suffix of the media reference type. 

    Example:
        ```
        # Frame start = 1
        # Frame step = 3
        # Number of images in sequence = 3
        # Frame zero padding = 4
        target_url_range = "file://some/base/directory/show_shot.0000{1..10..3}.exr"

        # Frame start = 0
        # Frame step = 2
        # Number of images in sequence = 10
        # Frame zero padding = 1
        target_url_range = "file://some/dir/foo_shot.0{0..20..2}.exr"
        ```
    """

    @staticmethod
    def draw_info(
        clip: otio.schema.Clip, svg_writer: SVGWriter, media_origin: Point
    ):
        # Draw available range
        if clip.available_range() is None:
            available_range_text = r"available_range: {}".format("None")
        else:
            available_range_text = r"available_range: {}, {}".format(
                repr(float(round(clip.available_range().start_time.value, 1))),
                repr(float(round(clip.available_range().duration.value, 1))),
            )
        available_range_location = Point(
            media_origin.x + svg_writer.font_size,
            media_origin.y - svg_writer.font_size,
        )
        svg_writer.draw_text(
            available_range_text,
            available_range_location,
            svg_writer.font_size,
        )

        media_ref = clip.media_reference

        # Draw target ranged url
        step = media_ref.frame_step
        start = media_ref.start_frame
        end = start + (step * (media_ref.number_of_images_in_sequence() - 1))

        symbol = (
            f"{'0' * media_ref.frame_zero_padding}{{{start}..{end}..{step}}}"
        )

        target_url_text = (
            f"target_url_range={media_ref.abstract_target_url(symbol)}"
        )

        target_url_location = Point(
            media_origin.x + svg_writer.font_size,
            media_origin.y - 2.0 * svg_writer.font_size,
        )
        svg_writer.draw_text(
            target_url_text, target_url_location, svg_writer.font_size
        )


class DefaultMediaReferenceHandler(MediaReferenceInfoHandler):
    """
    Default fallback for drawing media reference info with the SVG Writer
    """

    @staticmethod
    def draw_info(
        clip: otio.schema.Clip, svg_writer: SVGWriter, media_origin: Point
    ):
        # Draw available range
        if clip.available_range() is None:
            available_range_text = r"available_range: {}".format("None")
        else:
            available_range_text = r"available_range: {}, {}".format(
                repr(float(round(clip.available_range().start_time.value, 1))),
                repr(float(round(clip.available_range().duration.value, 1))),
            )
        available_range_location = Point(
            media_origin.x + svg_writer.font_size,
            media_origin.y - svg_writer.font_size,
        )
        svg_writer.draw_text(
            available_range_text,
            available_range_location,
            svg_writer.font_size,
        )

        media_ref = clip.media_reference

        # Draw target url
        if hasattr(media_ref, "target_url") and media_ref.target_url is None:
            target_url_text = r"target_url: {}".format("Media Unavailable")
        else:
            target_url_text = rf"target_url: {media_ref.target_url}"
        target_url_location = Point(
            media_origin.x + svg_writer.font_size,
            media_origin.y - 2.0 * svg_writer.font_size,
        )
        svg_writer.draw_text(
            target_url_text, target_url_location, svg_writer.font_size
        )
