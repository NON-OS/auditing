# WS6. Devices, DMA and firmware

The boundary between capsules and hardware, and between the kernel and untrusted devices.

## Look for

- [ ] PCI enumeration, BAR mapping and interrupt handling driven by device data.
- [ ] The MSI broker: confirm nothing else can enable a message interrupt.
- [ ] DMA containment when the IOMMU tables are absent or unusable. Establish what stops a device capsule or a device from reaching kernel and other capsules' memory, in every profile.
- [ ] DMA containment when the IOMMU is present: domain setup and teardown.
- [ ] Device parsers for untrusted hardware data (USB descriptors, storage and virtio structures, Wi-Fi and Bluetooth frames, smart card and FIDO transports).
- [ ] Firmware blobs: how a blob is verified before it is loaded.

## Evidence to keep

- A table of device class against containment in each profile.
- Fuzz corpora for each parser.

## Notes

Engagement notes for this workstream are kept privately until each finding has been disclosed. Do not add unfixed findings to this file.
