new-post slug:
    echo '+++' > "content/{{slug}}.md"
    echo 'title = ""' >> "content/{{slug}}.md"
    echo "date = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"" >> "content/{{slug}}.md"
    echo '[taxonomies]' >> "content/{{slug}}.md"
    echo 'tags = []' >> "content/{{slug}}.md"
    echo 'categories = []' >> "content/{{slug}}.md"
    echo '+++' >> "content/{{slug}}.md"

fix:
    pre-commit run --all-files

prepare-image img:
    exiftool -c "%.6f" -LensModel -ISO -ExposureTime -ImageSize -GPSPosition \
        -GPSAltitude -GPSImgDirection -CreateDate -h {{img}}
    exiftool -overwrite_original -All= -TagsFromFile @ -ColorSpaceTags {{img}}
