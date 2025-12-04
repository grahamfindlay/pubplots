# Pros, cons, and "gotchas" for various vector graphics editors

This document summarizes some pros, cons, and common pitfalls to avoid when preparing figures for publication.

## Figma

Figma is nearly perfect for combining figure elements and laying out families of multi-panel figures (or posters) with consistent styling. It is easy, fast, powerful, platform-agnostic, and students can use it without an expensive license. However, Figma has several interoperability issues with other vector graphics editors used by publishers, especially Adobe Illustrator. In addition to a funky exporter, it also has an importer that mangles many SVGs created by other programs. Use Figma with caution, because when it comes to the post-acceptance production process, that's when the issues can become deeply problematic. I had to remake nearly all of my 20 figures from scratch after acceptance for one paper because of Figma-related issues. And I *still* try to use Figma. For me, the only real alternative is [Affinity Studio](#affinity-studio).

Pros:

- You can resize SVG elements *without* resizing text.

Cons:

- You cannot resize SVG elements *and* resize line weights proportionally (unless you rasterize the image, which you should never do).

Gotchas:

- First, see the issues with scaling mentioned in the [README](../README.md#figma-specific-scaling).
- SVGs exported from R using the standard, modern `svglite` backend are generally mangled by Figma's importer. Shaded error bands, for example, are irredeemably broken. As a workaround, use the older `svg` device from the `grDevices` package. I have tried getting LLMs to post-process SVGs to fix interoperability issues, but with limited success.
- Figma exports PDFs in a way that are virtually never correctly imported by vector graphics editors like Adobe Illustrator, Affinity Designer, or Inkscape. Avoid exporting PDFs from Figma if you intend to edit them in another program, or provide them to a publisher.
- Figma's exports SVGs that are more likely to be correctly imported by other vector graphics editors. However, Figma SVGs still have some issues (e.g., embedded raster elements are indirectly referenced, which trips up Illustrator). Test your workflow thoroughly if you intend to use Figma SVGs elsewhere.

## Adobe Illustrator

Pros:

- Virtually guarantees that your outputs will be accepted with minimal hassle by publishers.

Cons:

- You cannot resize SVG elements without resizing text. This is a dealbreaker for me.

Gotchas:

- None so far!

## Affinity Studio

Formerly Affinity Designer, now part of Affinity Studio, which also includes Affinity Photo and Affinity Publisher. Uses a freemium model, which I'm leery of, but it seems the plan for monetization is just to make AI features subscription based, which is tolerable.

Pros:

- Allows selectively resizing text, line weights, and other elements when resizing SVGs.
- Supports exports in a wide variety of formats, and interoperability with Adobe Illustrator, other vector graphics editors, and publishsing software seems good.

Cons:

- The SVG import process is *extremeley* clunky. It involves first importing the SVG as an embedded document, opening it in a separate window, grouping the top-level layers, and cutting-and-pasting them (losing the filename in the process) into the desired artboard. This is a huge pain if you have many subplots to process. If only this process could be scripted...
- Several defaults (e.g. snapping) are un-intuitive and must be manually changed. But at least you *can* do just about anything with sufficient effort.

Gotchas

- None so far!

## Inskscape

The [Scientific Inskscape extension](https://github.com/burghoff/Scientific-Inkscape) is a must.

Pros:

- Free and open source.
- SVGs can be scaled without scaling text or tickmarks (requires extension).

Cons:

- You cannot have multiple artboards in a single document, which is a dealbreaker for me.
