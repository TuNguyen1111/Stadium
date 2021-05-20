
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var oldValuesTimeFrames = getStadiumTimeFramesInformation()
var oldValuesDetail =  getStadiumInformation()

initScreen()

function initScreen() { 
    setEventForPencilsIcon()
    addEventInput()
    changeSelectTag()
    sendData()
    setEventForStars()
    setUserStarRating()
    getAverageUsersRating()
}




function getInput() {
    let getData = this.getAttribute('data-name')
    let dataCheck = this.getAttribute('data-check')
    let checkBox = document.getElementById(dataCheck)

    let input = document.getElementById(getData)
    if (input.disabled) {
        input.disabled = false
    } else {
        input.disabled = true
    }

    if ( checkBox ) {
        if ( checkBox.disabled ) {
            checkBox.disabled = false
        } else {
            checkBox.disabled = true
        }

    }
}

function setEventForPencilsIcon() {
    let pencils = document.querySelectorAll('i')
    for (let pencil of pencils) { 
        pencil.addEventListener('click', getInput)
    }
}

function getStadiumInformation() {
    let oldValuesDetail = {}

    for (let item of stadiumFormDetail) {
        oldValuesDetail[item.id] = item.value
    } 
    return oldValuesDetail      
}

function getStadiumTimeFramesInformation() {
    let oldValuesTimeFrames = {}

    for (let item of stadiumFormTimeFrames) {
        if (item.checked || !item.checked) {
            oldValuesTimeFrames[item.id] = item.checked
        } else {  
            oldValuesTimeFrames[item.id] = item.value
        }
    }
    return oldValuesTimeFrames
}

function checkValueOfDetailInput() {
    let current = this.value
    let saveBtn = document.getElementById('saveDetailBtn')
    
    if (current != oldValuesDetail[this.id]) {
        saveBtn.disabled = false
        for (let item of stadiumFormDetail){
            item.disabled = false
        }
    } else {
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
        for (let item of stadiumFormTimeFrames){
            item.disabled = false
        }
    } else {
        saveBtn.disabled = true
    }
}

function addEventInput() {
    for (let item of stadiumFormDetail) {
        item.addEventListener('input', checkValueOfDetailInput)
    }
    for (let item of stadiumFormTimeFrames) {
        item.addEventListener('input', checkValueOfTimeFrameInput)
        item.disabled = true
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
    for (let item of inputTags) {
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
    const starType = [oneStar, twoStar, threeStar, fourStar, fiveStar]

    starType.forEach(item => {
        item.addEventListener('click', function(e) {
            handleStarSelect(e.target.id)
        })
    });
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

    for (let [index, children] of spanChildrens.entries()) {
        if (index < size) {
            children.classList.add('checked')
            children.setAttribute('point', index+1)
        } else {
            children.classList.remove('checked')
            children.setAttribute('point', 0)
        }
    }
}

function sendData() {
    let commentContent = document.getElementById('comment-input')
    let csrf = document.getElementsByName('csrfmiddlewaretoken')
    let commentBtn = document.getElementById('comment-btn')
    let stadiumId = document.getElementById('stadium-id').value

    commentBtn.addEventListener('click', (e) => {
        e.preventDefault() 
        let spanChildrens = document.getElementById('star-rating').children
        var starPoint = 0
        spanChildrens = [].slice.call(spanChildrens, 0).reverse()

        for (let item of spanChildrens) {
            itemPoint = item.getAttribute('point')
            if (itemPoint > 0) {
                starPoint = itemPoint
            }
        }

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
                let totalOfStarTypeRated = data.stars_type_rated_numbers
                console.log(totalOfStarTypeRated)
                handleDataRespone(data)
                clearInputAndStar(commentContent)
                getTotalOfStarType(totalOfStarTypeRated)
            },
            error: (error) => {
                console.log(error)
            }
        })
    })
}

function handleDataRespone(data) {
    let userRated = data.user_rated_information
    let allCommentsDiv = document.getElementById('all-comments')

    createElementForUserRated(userRated, allCommentsDiv)
}

function setUserStarRating() {
    let allUsersStarRating = document.querySelectorAll('.user-star-rating')

    for (let userStarRating of allUsersStarRating ) {
        let childrenElements = userStarRating.children
        userStarRating = childrenElements[childrenElements.length - 1].value
        childrenElements = Array.from(childrenElements);

        for (let [index, childrenElement] of childrenElements.entries()) {
            if (index < userStarRating) {
                childrenElement.classList.add('checked')
            }
        }

    }
}

function clearInputAndStar(commentContent) {
    let starRatingInput = document.getElementById('star-rating')
    let childrenElements = starRatingInput.children

    for (let childrenElement of childrenElements) {
        childrenElement.classList.remove('checked')
    }

    commentContent.value = ''
}

function getAverageUsersRating() {
    let stadiumId = document.getElementById('stadium-id').value
    $.ajax({
        type: 'get',
        url: '/danh-gia/',
        data: {
            stadiumId: stadiumId
        },
        success: function(data) {
            let totalOfStarTypeRated = data.stars_type_rated_numbers

            getTotalOfStarType(totalOfStarTypeRated)
            setEventForStarTypeBtn(data)
        },
        error: function(error) {
            console.log(error)
        }
    })
}

function getTotalOfStarType(totalOfStarTypeRated) {
    let allStarRateBtns = document.querySelectorAll('.star-rate-btn')

    for (const [star, totalStar] of Object.entries(totalOfStarTypeRated)) {
        for (let starRateBtn of allStarRateBtns) {
            if (starRateBtn.id === star) {
                let typeOfStar = starRateBtn.getAttribute('star-type')
                starRateBtn.innerHTML = `${typeOfStar} sao (${totalStar})`
            }
        }
    }
}

function setEventForStarTypeBtn(data) {
    let summaryOfStarsType = data.summary_of_stars_type
    let allStarRateTypeBtns = document.querySelectorAll('.star-rate-btn')

    for (let starRateTypeBtn of allStarRateTypeBtns) {
        starRateTypeBtn.addEventListener('click', function() {
            let starRateTypeBtnId = starRateTypeBtn.id
            var allCommentsDiv = document.getElementById('all-comments')
            allCommentsDiv.innerHTML = ''

            for (const [starType, allUsersRated] of Object.entries(summaryOfStarsType)) {

                if (starType === starRateTypeBtnId) {
                    for (let userRated of allUsersRated) {
                        createElementForUserRated(userRated, allCommentsDiv)
                    }
                }
            }
        })
    }
}

function createElementForUserRated(userRated, allCommentsDiv) {
    let username = userRated.username
    let commentContent = userRated.comment
    let star_point = userRated.star_point
    let commentDiv = document.createElement('div')
    let aTag = document.createElement('a')
    let h4Tag = document.createElement('h4')
    let userStarRatingDiv = document.createElement('div')
    let starPointInput = document.createElement('input')
    let hrTag = document.createElement('hr')

    for (let i = 0; i < 5; i++) {
        let spanTag = document.createElement('span')
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
    allCommentsDiv.appendChild(hrTag)
    setUserStarRating()
}

