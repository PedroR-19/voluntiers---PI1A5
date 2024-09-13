document.addEventListener('DOMContentLoaded', function() {
    const countryField     = document.getElementById('id_country');
    const stateField       = document.getElementById('id_state');
    const cityField        = document.getElementById('id_city');
    const categoryField    = document.getElementById('id_category');
    const subcategoryField = document.getElementById('id_subcategory');

    countryField.addEventListener('change', function() {
        const country = countryField.value;
        fetch(`/ajax/filter-states/?country=${country}`)
            .then(response => response.json())
            .then(states => {
                stateField.innerHTML = '';
                states.forEach(state => {
                    const option = document.createElement('option');
                    option.value = state[0];
                    option.text = state[1];
                    stateField.appendChild(option);
                });
                cityField.innerHTML = '';  // Clear city field when country changes
            });
    });

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
