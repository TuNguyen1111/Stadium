// var inputFields = document.querySelectorAll('input')
var pencils = document.querySelectorAll('i')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
console.log(stadiumFormTimeFrames)

var oldValuesDetail = {}
var oldValuesTimeFrames = {}

const commentInput = document.getElementById('comment-input')

for (let i = 1; i < stadiumFormDetail.length; i++) {
    oldValuesDetail[stadiumFormDetail[i].id] = stadiumFormDetail[i].value
}

for (let i = 1; i < stadiumFormTimeFrames.length; i++) {
    if ( stadiumFormTimeFrames[i].checked || !stadiumFormTimeFrames[i].checked ) {
        oldValuesTimeFrames[stadiumFormTimeFrames[i].id] = stadiumFormTimeFrames[i].checked
    }else{
        oldValuesTimeFrames[stadiumFormTimeFrames[i].id] = stadiumFormTimeFrames[i].value
    }

}

function getInput() {
    let getData = this.getAttribute('data-name')
    let dataCheck = this.getAttribute('data-check')
    let checkBox = document.getElementById(dataCheck)

    let input = document.getElementById(getData)
    if (input.disabled) {
        input.disabled = false
    }else {
        input.disabled = true
    }

    if ( checkBox ) {
        if ( checkBox.disabled ) {
            checkBox.disabled = false
        }else {
            checkBox.disabled = true
        }

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
    if (this.checked) {
        current = this.checked
    }

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

function turnOnDeleteModal() {
    let modalDelete = new bootstrap.Modal(document.getElementById('delete-form-modal'));
    modalDelete.show()
}

function tunrOndeleteTimeFrameModal(id) {
    let timeframeDeleteModal = new bootstrap.Modal(document.getElementById(`delete-timeframe-${id}`))
    timeframeDeleteModal.show()
}
