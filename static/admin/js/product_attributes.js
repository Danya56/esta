document.addEventListener('DOMContentLoaded', function() {
    const categoryField = document.getElementById("id_category");
    const baseUrl = window.location.origin;

    function updateAttributes(categoryId) {
        const selects = document.querySelectorAll('select[name$="-attribute"]')
        
        if (!categoryId) {
            selects.forEach(select => {
                select.innerHTML = '<option value="">---------</option>';
            })
            return;
        };

        fetch(`${baseUrl}/products/get-attributes/?category_id=${categoryId}`)
        .then(response => response.json())
        .then(data => {
            selects.forEach(select => {
                const currentValue = select.value;
                
                select.innerHTML = '<option value="">-------</option>'
                    
                data.forEach(attr => {
                    const option = document.createElement('option');
                    option.value = attr.id;
                    option.textContent = attr.name;
                    select.appendChild(option);
                });
            });
        })
        .catch(error => console.error('Ошибка: ', error));
    }

    if (!categoryField.value) {
        console.log('Zdarova')
        updateAttributes(this.value);
    }

    categoryField.addEventListener('change', function() {
        updateAttributes(this.value);
    });
})