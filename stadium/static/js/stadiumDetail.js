// var inputFields = document.querySelectorAll('input')
var pencils = document.querySelectorAll('i')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
var oldValuesDetail = {}
var oldValuesTimeFrames = {}

for (let i = 1; i < stadiumFormDetail.length; i++) {
    oldValuesDetail[stadiumFormDetail[i].id] = stadiumFormDetail[i].value
}
console.log(oldValuesDetail)
for (let i = 1; i < stadiumFormTimeFrames.length; i++) {
    oldValuesTimeFrames[stadiumFormTimeFrames[i].id] = stadiumFormTimeFrames[i].value
}

function getInput() {
    let getData = this.getAttribute('data-name')
    let input = document.getElementById(getData)
    if (input.disabled) {
        input.disabled = false
    }else {
        input.disabled = true

    }
}

for (let i = 0; i < pencils.length;i++) {
    pencils[i].addEventListener('click', getInput)
}


function checkValueOfDetailInput() {
    let current = this.value
    let saveBtn = document.getElementById('saveDetailBtn')
    if (current != oldValuesDetail[this.id]) {
        saveBtn.disabled = false
        for (let i = 0; i < stadiumFormDetail.length; i++){
            stadiumFormDetail[i].disabled = false
        }
    }else {
        saveBtn.disabled = true

    }
}

function checkValueOfTimeFrameInput() {
    let current = this.value
    let saveBtn = document.getElementById('saveTimeFramesBtn')
    if (current != oldValuesTimeFrames[this.id]) {
        saveBtn.disabled = false
        for (let i = 0; i < stadiumFormTimeFrames.length; i++){
            stadiumFormTimeFrames[i].disabled = false
        }
    }else {
        saveBtn.disabled = true
    }
}

function addEventInput() {
    for (let i = 1; i < stadiumFormDetail.length; i++) {
        stadiumFormDetail[i].addEventListener('input', checkValueOfDetailInput)
    }
    for (let i = 1; i < stadiumFormTimeFrames.length; i++) {
        stadiumFormTimeFrames[i].addEventListener('input', checkValueOfTimeFrameInput)
        stadiumFormTimeFrames[i].disabled = true
    }
}

addEventInput()

// function hiddenSelect() {
//     let selectTags = document.querySelectorAll('select')
//     for (let i = 0; i < selectTags.length; i++) {
//         let item = selectTags[i]
//         item.style.display = 'none'
//         let pTag = document.createElement('span')
//         let value = item.options[item.selectedIndex].text;
//         pTag.innerHTML = value
//         item.parentNode.insertBefore(pTag, item.nextSibling)
//     }
// }
// hiddenSelect()

function turnOnDeleteModal() {
    let modalDelete = new bootstrap.Modal(document.getElementById('delete-form-modal'));
    modalDelete.show()
}

