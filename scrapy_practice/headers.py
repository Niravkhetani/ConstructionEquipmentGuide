from fake_headers import Headers

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)
header1=None
for i in range(10):
    header1=header.generate()

print(header1)
