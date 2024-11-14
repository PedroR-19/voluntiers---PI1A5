const masks = {
    name (value) {
        return value
        .replace(/[^A-ü ]+/g, '')
        .replace(/([A-ü ]{50})[A-ü ]+?$/, '$1')
        .replace(/^ /g, '')
        .replace(/(\s|^)[A-ü]/g, function(match) { return match.toUpperCase(); })
        .replace(/ +/g, ' ')
        // .replace(/[~^´`¨]/g, '');
      },

    institution_name (value) {
        return value
        // .replace(/[^A-ü ]+/g, '')
        .replace(/([A-ü ]{50})[A-ü ]+?$/, '$1')
        .replace(/^ /g, '')
        .replace(/(\s|^)[A-ü]/g, function(match) { return match.toUpperCase(); })
        .replace(/ +/g, ' ')
        // .replace(/[~^´`¨]/g, '');
      },

    cpf (value) {
        return value
        .replace(/\D+/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})/, '$1-$2')
        .replace(/(-\d{2})\d+?$/, '$1')
    },

    cnpj (value) {
        return value
        .replace(/\D+/g, '')
        .replace(/(\d{2})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,4})/, '$1/$2')
        .replace(/(\/\d{4})(\d{1,2})/, '$1-$2')
        .replace(/(\/\d{4}-\d{2})\d+?$/, '$1')
    },

    cep (value) {
        return value
        .replace(/\D+/g, '')
        .replace(/(\d{5})(\d)/, '$1-$2')
        .replace(/(-\d{3})\d+?$/, '$1')
    },

    about (value) {
        return value
        .replace(/[^A-ü ]+/g, '')
        .replace(/([A-ü ]{300})[A-ü ]+?$/, '$1')
        .replace(/^ /g, '')
        // .replace(/(\s|^)[A-ü]/g, function(match) { return match.toUpperCase(); })
        .replace(/ +/g, ' ')
    }

    // date (value) {
    //     return value
    //     .replace(/\D+/g, '')
    //     .replace(/(\d{2})(\d)/, '$1/$2')
    //     .replace(/(\/\d{2})(\d)/, '$1/$2')
    //     .replace(/(\/\d{4})\d+?$/, '$1')
    // },
  
    // phone (value) {
    //     return value
    //     .replace(/\D+/g, '')
    //     .replace(/(\d{2})(\d)/, '($1) $2')
    //     .replace(/(\d{4})(\d)/, '$1-$2')
    //     .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
    //     .replace(/(-\d{4})\d+?$/, '$1')
    // },

    // money (value) {
    //     const cleanValue = +value.replace(/\D+/g, '').substring(0, 11);
    //     const options = { style: 'currency', currency: 'BRL' };
    //     return new Intl.NumberFormat('pt-br', options).format(parseInt(cleanValue) / 100);
    // }
}

const id_cpf = document.getElementById('id_cpf')
const id_cnpj = document.getElementById('id_cnpj')
const id_cep = document.getElementById('id_cep')

const id_first_name = document.getElementById('id_first_name')
const id_last_name = document.getElementById('id_last_name')
const id_name = document.getElementById('id_name')

const id_about = document.getElementById('id_about')

if (id_cpf) {
    id_cpf.addEventListener('input', e => {
        e.target.value = masks.cpf(e.target.value)
    }, false)
}

if (id_cnpj) {
    id_cnpj.addEventListener('input', e => {
        e.target.value = masks.cnpj(e.target.value)
    }, false)
}

if (id_cep) {
    id_cep.addEventListener('input', e => {
        e.target.value = masks.cep(e.target.value)
    }, false)
}

if (id_first_name) {
    id_first_name.addEventListener('input', e => {
        e.target.value = masks.name(e.target.value)
    }, false)
}

if (id_last_name) {
    id_last_name.addEventListener('input', e => {
        e.target.value = masks.name(e.target.value)
    }, false)
}

if (id_name) {
    id_name.addEventListener('input', e => {
        e.target.value = masks.institution_name(e.target.value)
    }, false)
}

if (id_about) {
    id_about.addEventListener('input', e => {
        e.target.value = masks.about(e.target.value)
    }, false)
}