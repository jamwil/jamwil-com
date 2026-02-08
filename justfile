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

# Install JS tooling used by fmt/ci
deps:
    npm install

# Local formatting (writes changes)
fmt:
    npm exec -- prettier --ignore-path .prettierignore --ignore-unknown --write \
        config.toml content sass static templates

# Backwards-compatible name
fix: fmt

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

build-sdf: fmt
    zola build -u 'http://jamwil.sdf.org' -o docs_sdf -f

# CI entrypoint: never includes drafts
ci: fmt-check check
    zola build

# CI entrypoint for preview deployments (override base_url)
ci-preview base_url: fmt-check check
    zola build -u "{{base_url}}"

publish:
    ssh jamwil@tty.sdf.org -t "rm -rf html/*"
    scp -r docs_sdf/* jamwil@tty.sdf.org:html/
