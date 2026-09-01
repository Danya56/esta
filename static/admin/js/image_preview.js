document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('change', function(event) {
        if (event.target && event.target.type == 'file') {
            const input = event.target;
            const file = input.files[0];

            if (file) {
                const inlineRow = input.closest('.form-row');
                if (!inlineRow) return;
                let previewContainer = inlineRow.querySelector('.field-image_preview p');

                if (!previewContainer) {
                    previewContainer = inlineRow.querySelector('.field-image_preview div');
                }

                if (previewContainer) {
                    const blobUrl = URL.createObjectURL(file);

                    previewContainer.innerHTML = `<img src="${blobUrl}" style="max-height: 100px; max-width: 100px; object-fit: cover; border: 2px dashed #417690; padding: 2px;" />`
                }
            }
        }
    });
});