document.addEventListener('DOMContentLoaded', function() {
    const stateField       = document.getElementById('id_state');
    const cityField        = document.getElementById('id_city');
    const categoryField    = document.getElementById('id_category');
    const subcategoryField = document.getElementById('id_subcategory');

    stateField.addEventListener('change', function() {
        const state = stateField.value;
        fetch(`/ajax/filter-cities/?state=${state}`)
            .then(response => response.json())
            .then(cities => {
                cityField.innerHTML = '';
                cities.forEach(city => {
                    const option = document.createElement('option');
                    option.value = city[0];
                    option.text = city[1];
                    cityField.appendChild(option);
                });
            });
    });

    categoryField.addEventListener('change', function() {
        const categoryId = categoryField.value;
        fetch(`/ajax/filter-subcategories/?category_id=${categoryId}`)
            .then(response => response.json())
            .then(subcategories => {
                subcategoryField.innerHTML = '';
                subcategories.forEach(subcategory => {
                    const option = document.createElement('option');
                    option.value = subcategory.id;
                    option.text = subcategory.name;
                    subcategoryField.appendChild(option);
                });
            });
    });
});
