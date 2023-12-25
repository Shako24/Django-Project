totalService = 0

const services = [
    { value: 'basicExteriorWash' },
    { value: 'basicExteriorWashSUV' },
    { value: 'interiorCleaning' },
    { value: 'interiorCleaningSUV' },
    { value: 'BasicExteriorWithinteriorCleaning' },
    { value: 'BasicExteriorWithinteriorCleaningSUV' },
    { value: 'exteriorWashWithWax' },
    { value: 'exteriorWashWithWaxSUV' },
    { value: 'superDirtyExteriorWash' },
    { value: 'superDirtyExteriorWashSUV' },
    { value: 'engineDetailing' },
    { value: 'engineDetailingSUV' }
]

const options = [
    { value: 'basicExteriorWashOption' },
    { value: 'interiorCleaningOption' },
    { value: 'BasicExteriorWithinteriorCleaningOption' },
    { value: 'exteriorWashWithWaxOption' },
    { value: 'superDirtyExteriorWashOption' },
    { value: 'engineDetailingOption' },
    { value: 'testing' }
]

function buttonAdd(number) {
    const service = document.getElementById(services[number].value);
    if (parseInt(service.value) < 4 && totalService < 4) {
        service.value = parseInt(service.value) + 1;
        totalService += 1
    }
        
}

function buttonMinus(number) {
    const service = document.getElementById(services[number].value);
    if (parseInt(service.value) > 0) {
        service.value = parseInt(service.value) - 1;
        totalService -= 1
    }      
}

function showOption(number) {
    const container = $('#'+String(options[number].value));
    

    console.log(container.attr('id'))

    container.slideDown()

    const button = document.getElementById('cwsh-btn-'+number);
    
    button.style.opacity = 0
    button.style.transition = 'transform 0.5s, opacity 0.1s'
    button.style.transform = "translateX(-1000px)";
    button.style.disabled = true;

}

function removeOption(number) {
    const container = document.getElementById(options[number].value);
    container.style.opacity = '1';
    container.style.height = 'auto';
}