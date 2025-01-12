"""Prepare the given image and spit out a snippet."""

import click
from exiftool import ExifToolHelper


def decdeg2dms(dd):
    mult = -1 if dd < 0 else 1
    mnt,sec = divmod(abs(dd)*3600, 60)
    deg,mnt = divmod(mnt, 60)
    return mult*deg, mult*mnt, mult*sec


@click.command()
@click.argument('inputs', nargs=-1, required=True)
@click.option('--clean', '-c', is_flag=True, help="Clean the tags from the image.")
def main(inputs: list[str], clean: bool):
    """Strip exif data from the input images and prepare a zola snippet."""

    with ExifToolHelper(common_args=None) as eth:
        for input in inputs:
            coordinates = eth.execute_json(
                "-n",
                "-GPSLatitude",
                "-GPSLongitude",
                input
            )[0]

            lat_dir = "N" if coordinates['GPSLatitude'] >= 0 else "S"
            lon_dir = "E" if coordinates['GPSLongitude'] >0 else "W"

            lat = decdeg2dms(abs(coordinates['GPSLatitude']))
            lon = decdeg2dms(abs(coordinates['GPSLongitude']))

            r = round
            encoded_dms = f"{r(lat[0])}_{r(lat[1])}_{r(lat[2])}_{lat_dir}_{r(lon[0])}_{r(lon[1])}_{r(lon[2])}_{lon_dir}"
            geohack_url = f"https://geohack.toolforge.org/geohack.php?params={encoded_dms}"

            display_tags = eth.execute_json(
                "-c",
                "%.6f",
                "-Make",
                "-Model",
                "-LensModel",
                "-ExposureTime",
                "-FNumber",
                "-ISO",
                "-FocalLength",
                "-GPSPosition",
                "-GPSAltitude",
                "-ImageSize",
                "-FileSize",
                input
            )[0]

            lines = [f"<!-- {input} -->", "<table>"]
            for key, value in display_tags.items():
                if key == "SourceFile":
                    continue

                match key:
                    case 'Make':
                        desc = "Make"
                    case 'Model':
                        desc = "Camera Model Name"
                    case 'LensModel':
                        desc = "Lens Model"
                    case 'ExposureTime':
                        desc = "Exposure Time"
                    case 'FNumber':
                        desc = "F Number"
                    case 'ISO':
                        desc = "ISO"
                    case 'FocalLength':
                        desc = "Focal Length"
                    case 'GPSPosition':
                        desc = "GPS Position"
                        value = f'<a href="{geohack_url}" target="_blank">{value} ⤴︎</a>'
                    case 'GPSAltitude':
                        desc = "GPS Altitude"
                    case 'ImageSize':
                        desc = "Image Size"
                    case 'FileSize':
                        desc = "File Size"
                    case _:
                        desc = key
                
                lines.append(f"<tr><td>{desc}</td><td>{value}</td></tr>")
            
            reduced_path = input.replace("content/", "", 1).replace("_", "-").replace("IMG-", "IMG_")
            lines.append("<tr><td colspan=2>{{ image_link(path='%s', text='View full resolution') }}</td></tr>" % (reduced_path,))

            lines.append("</table>")

            table = "\n".join(lines)

            output = [
                '{{ resize_image(path="%s", width=500, height=500, op="fit_width", alt="") }}' % (input,),
                "",
                table,
                "",
                '<div style="clear:both;"></div>',
                "",
            ]

            click.echo("\n".join(output))

            if clean:
                eth.execute(
                    "-All=",
                    '-IPTC:CopyrightNotice="© James Williams"',
                    '-TagsFromFile',
                    '@',
                    '-ColorSpaceTags',
                    '-Orientation',
                    input
                )

if __name__ == '__main__':
    main()

