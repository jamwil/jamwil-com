# Bootstrap a new post
new-post slug:
    echo '+++' > "content/{{ slug }}.md"
    echo 'title = ""' >> "content/{{ slug }}.md"
    echo "date = \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"" >> "content/{{ slug }}.md"
    echo 'draft = true' >> "content/{{ slug }}.md"
    echo '[taxonomies]' >> "content/{{ slug }}.md"
    echo 'tags = []' >> "content/{{ slug }}.md"
    echo 'categories = []' >> "content/{{ slug }}.md"
    echo '+++' >> "content/{{ slug }}.md"

# Update the date on a post to now
update-date file:
    @-sed -i '' 's/^date = ".*"/date = "'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'"/' {{ file }}

# Prepare the tags and add a copyright
prepare-image img:
    exiftool -c "%.6f" -Make -Model -LensModel -ExposureTime -FNumber -ISO -FocalLength \
        -GPSPosition -GPSAltitude -ImageSize -FileSize -h {{ img }}
    exiftool -All= -IPTC:CopyrightNotice="© James Williams" -TagsFromFile @ -ColorSpaceTags -ICC_Profile -Orientation {{ img }}

# Geotag images based on a track, offset should be like '-07:00'
geotag-images-from-track track offset dir:
    exiftool -geotag {{ track }} '-geotime<${createdate}{{ offset }}' {{ dir }}

# Add manual coordinates to a photo's exif data
geotag-image lat lon img:
    exiftool -GPSLatitude={{ lat }} -GPSLatitudeRef={{ lat }} -GPSLongitude={{ lon }} -GPSLongitudeRef={{ lon }} {{ img }}

# Install JS tooling used by fmt/ci
deps:
    npm install

# Local formatting (writes changes)
fmt:
    npm exec -- prettier --ignore-path .prettierignore --ignore-unknown --write \
        config.toml content sass static templates

# CI formatting (fails if changes needed)
fmt-check:
    npm exec -- prettier --ignore-path .prettierignore --ignore-unknown --check \
        config.toml content sass static templates

# Lint/validate
check:
    zola check --skip-external-links

# Build targets
build: fmt
    zola build
    npm exec -- prettier --ignore-path .prettierignore --ignore-unknown --write public

# Publish the site
publish: build
    rsync -a --delete "public/" ubuntu@dedi2028:/srv/jamwil.com/
    ssh ubuntu@dedi2028 sudo chown -R root:caddy "/srv/jamwil.com"
    ssh ubuntu@dedi2028 sudo chmod -R 750 "/srv/jamwil.com"
