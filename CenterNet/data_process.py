def __getitem__(self, index):
    batch_hm = np.zeros((self.output_shape[0], self.output_shape[1], self.num_classes), dtype=np.float32)
    batch_wh = np.zeros((self.output_shape[0], self.output_shape[1], 2), dtype=np.float32)
    batch_offset = np.zeros((self.output_shape[0], self.output_shape[1], 2), dtype=np.float32)
    batch_offset_mask = np.zeros((self.output_shape[0], self.output_shape[1]), dtype=np.float32)

    # Read image and bounding boxes
    image, bboxes = self.parse_annotation(index)

    if self.is_train:
        image, bboxes = self.data_augmentation(image, bboxes)

    # Image preprocess
    image, bboxes = image_resize(image, self.input_shape, bboxes)
    image = preprocess_input(image)

    # Clip bounding boxes
    clip_bboxes = []
    labels = []
    for bbox in bboxes:
        x1, y1, x2, y2, label = bbox

        if x2 <= x1 or y2 <= y1:
            # Don't use such boxes as this may cause nan loss.
            continue

        x1 = int(np.clip(x1, 0, self.input_shape[1]))
        y1 = int(np.clip(y1, 0, self.input_shape[0]))
        x2 = int(np.clip(x2, 0, self.input_shape[1]))
        y2 = int(np.clip(y2, 0, self.input_shape[0]))
        # Clipping coordinates between 0 to image dimensions as negative values
        # or values greater than image dimensions may cause nan loss.
        clip_bboxes.append([x1, y1, x2, y2])
        labels.append(label)

    bboxes = np.array(clip_bboxes)
    labels = np.array(labels)

    if len(bboxes) != 0:
        labels = np.array(labels, dtype=np.float32)
        bboxes = np.array(bboxes[:, :4], dtype=np.float32)
        bboxes[:, [0, 2]] = np.clip(bboxes[:, [0, 2]] / self.stride, a_min=0, a_max=self.output_shape[1])
        bboxes[:, [1, 3]] = np.clip(bboxes[:, [1, 3]] / self.stride, a_min=0, a_max=self.output_shape[0])

    for i in range(len(labels)):
        x1, y1, x2, y2 = bboxes[i]
        cls_id = int(labels[i])

        h, w = y2 - y1, x2 - x1
        if h > 0 and w > 0:
            radius = gaussian_radius((math.ceil(h), math.ceil(w)))
            radius = max(0, int(radius))

            # Calculates the feature points of the real box
            ct = np.array([(x1 + x2) / 2, (y1 + y2) / 2], dtype=np.float32)
            ct_int = ct.astype(np.int32)

            # Get gaussian heat map
            batch_hm[:, :, cls_id] = draw_gaussian(batch_hm[:, :, cls_id], ct_int, radius)

            # Assign ground truth height and width
            batch_wh[ct_int[1], ct_int[0]] = 1. * w, 1. * h

            # Assign center point offset
            batch_offset[ct_int[1], ct_int[0]] = ct - ct_int

            # Set the corresponding mask to 1
            batch_offset_mask[ct_int[1], ct_int[0]] = 1

    return image, batch_hm, batch_wh, batch_offset, batch_offset_mask
