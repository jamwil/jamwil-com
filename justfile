new-post slug:
    echo '+++' > "content/{{slug}}.md"
    echo 'title = ""' >> "content/{{slug}}.md"
    echo "date = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"" >> "content/{{slug}}.md"
    echo 'draft = true' >> "content/{{slug}}.md"
    echo '[taxonomies]' >> "content/{{slug}}.md"
    echo 'tags = []' >> "content/{{slug}}.md"
    echo 'categories = []' >> "content/{{slug}}.md"
    echo '+++' >> "content/{{slug}}.md"

prepare-image img:
    exiftool -c "%.6f" -Make -Model -LensModel -ExposureTime -FNumber -ISO -FocalLength \
        -GPSPosition -GPSAltitude -ImageSize -FileSize -h {{img}}
    exiftool -All= -IPTC:CopyrightNotice="© James Williams" -TagsFromFile @ -ColorSpaceTags -Orientation {{img}}

geotag-images-from-track track dir:
    exiftool -geotag {{track}} '-geotime<${createdate}-07:00' {{dir}}

geotag-image lat lon img:
    exiftool -GPSLatitude={{lat}} -GPSLatitudeRef={{lat}} -GPSLongitude={{lon}} -GPSLongitudeRef={{lon}} {{img}}

fix:
    npx prettier --ignore-path .prettierignore --ignore-unknown --write content docs docs_sdf sass templates

build: && fix
    zola build
    zola build -u 'http://jamwil.sdf.org' --drafts -o docs_sdf -f

publish:
    ssh jamwil@tty.sdf.org -t "rm -rf html/*"
    scp -r docs_sdf/* jamwil@tty.sdf.org:html/

