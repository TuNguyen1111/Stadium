// var inputFields = document.querySelectorAll('input')
var pencils = document.querySelectorAll('i')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
var oldValuesDetail = {}
var oldValuesTimeFrames = {}
const commentInput = document.getElementById('comment-input')

executeFunctions()

function executeFunctions() {
    addEventInput()
    changeSelectTag()
    sendData()
    setEventForStars()
    setUserStarRating()
}

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

function turnOnDeleteModal() {
    let modalDelete = new bootstrap.Modal(document.getElementById('delete-form-modal'));
    modalDelete.show()
}

function tunrOndeleteTimeFrameModal(id) {
    let timeframeDeleteModal = new bootstrap.Modal(document.getElementById(`delete-timeframe-${id}`))
    timeframeDeleteModal.show()
}

function changeSelectTag() {
    let inputTags = document.querySelectorAll('select')
    for (let i = 0; i < inputTags.length; i++) {
    let item = inputTags[i]
        let pTag = document.createElement('p')
        let value = item.options[item.selectedIndex].text;
        pTag.innerHTML = value
        item.parentNode.replaceChild(pTag, item)
    }
}

function setEventForStars() {
    const oneStar = document.getElementById('one-star')
    const twoStar = document.getElementById('two-star')
    const threeStar = document.getElementById('three-star')
    const fourStar = document.getElementById('four-star')
    const fiveStar = document.getElementById('five-star')
    var starPoint = 0
    const starArr = [oneStar, twoStar, threeStar, fourStar, fiveStar]

    starArr.forEach(item => {
        item.addEventListener('click', function(e) {
            handleStarSelect(e.target.id)
        })
    });
    
    console.log(document.getElementById('star-rating').children)
}

function handleStarSelect(starId) {
    switch(starId) {
        case 'one-star': {
            addOrRemoveCheckedClass(1)
            return
        }
        case 'two-star': {
            addOrRemoveCheckedClass(2)
            return
        }
        case 'three-star': {
            addOrRemoveCheckedClass(3)
            return
        }
        case 'four-star': {
            addOrRemoveCheckedClass(4)
            return
        }
        case 'five-star': {
            addOrRemoveCheckedClass(5)
            return
        }
    }
}

function addOrRemoveCheckedClass(size) {
    var spanChildrens = document.getElementById('star-rating').children
    spanChildrens = [].slice.call(spanChildrens, 0).reverse()
    for (let i = 0; i < spanChildrens.length; i++) {
        if (i < size) {
            spanChildrens[i].classList.add('checked')
            spanChildrens[i].setAttribute('point', i+1)
        }else {
            spanChildrens[i].classList.remove('checked')
            spanChildrens[i].setAttribute('point', 0)
        }
    }
}

function sendData() {
    let commentContent = document.getElementById('comment-input')
    let csrf = document.getElementsByName('csrfmiddlewaretoken')
    let commentBtn = document.getElementById('comment-btn')
    let stadiumId = document.getElementById('stadium-id').value

    commentBtn.addEventListener('click', (e) => {
        console.log('cliked')
        let spanChildrens = document.getElementById('star-rating').children
        var starPoint = 0
        spanChildrens = [].slice.call(spanChildrens, 0).reverse()
        
        for (let i = 0; i < spanChildrens.length; i++) {
            item = spanChildrens[i]
            itemPoint = item.getAttribute('point')
            if (itemPoint > 0) {
                starPoint = itemPoint
            }
        }
        
        e.preventDefault()
        $.ajax({
            type: 'post',
            url: '/danh-gia/',
            data: {
                commentData: commentContent.value,
                starPoint: starPoint,
                stadiumId: stadiumId,
                csrfmiddlewaretoken: csrf[0].value
            },
            success: (data) => {

                handleDataRespone(data)
                clearInputAndStar(commentContent)

            },
            error: (error) => {
                console.log(error)
            }
        })
    })
}

function handleDataRespone(data) {
    userCommentInfor = data.data_respone
    username = userCommentInfor.username
    commentContent = userCommentInfor.comment
    star_point = userCommentInfor.star_point
    
    allCommentsDiv = document.getElementById('all-comments')
    commentDiv = document.createElement('div')
    aTag = document.createElement('a')
    h4Tag = document.createElement('h4')
    userStarRatingDiv = document.createElement('div')
    starPointInput = document.createElement('input')

    for (let i = 0; i < 5; i++) {
        spanTag = document.createElement('span')
        spanTag.className = 'fa fa-star'
        spanTag.id = `user-${i + 1}-star`
        userStarRatingDiv.appendChild(spanTag)
    }

    commentDiv.className = 'comment-infor'
    userStarRatingDiv.className = 'user-star-rating'
    userStarRatingDiv.id = 'userStarRatingDiv'
    aTag.className = 'mr-2'
    starPointInput.type = 'hidden'
    starPointInput.id = 'user-star-point-rating'
    starPointInput.value = star_point

    aTag.innerHTML = username
    h4Tag.innerHTML = commentContent

    userStarRatingDiv.appendChild(starPointInput)
    commentDiv.appendChild(aTag)
    commentDiv.appendChild(h4Tag)
    commentDiv.appendChild(userStarRatingDiv)

    allCommentsDiv.appendChild(commentDiv)
    setUserStarRating()
}

function setUserStarRating() {
    let allUsersStarRating = document.querySelectorAll('.user-star-rating')

    for (let i = 0; i < allUsersStarRating.length; i++ ) {
        let userStarRating = allUsersStarRating[i]
        childrenElements = userStarRating.children
        userStarRating = childrenElements[childrenElements.length - 1].value

        for (let j = 0; j < childrenElements.length; j++) {
            if (j < userStarRating) {
                childrenElements[j].classList.add('checked')
            }
        }

    }
}

function clearInputAndStar(commentContent) {
    let starRatingInput = document.getElementById('star-rating')
    let childrenElements = starRatingInput.children

    for (let i = 0; i < childrenElements.length; i++) {
        childrenElements[i].classList.remove('checked')
    }

    commentContent.value = ''
}