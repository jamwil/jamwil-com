fix:
    pre-commit run --all-files

prepare-image img:
    exiftool -c "%.6f" -LensModel -ISO -ExposureTime -ImageSize -GPSPosition \
        -GPSAltitude -GPSImgDirection -CreateDate -h {{img}}
    exiftool -all= {{img}}