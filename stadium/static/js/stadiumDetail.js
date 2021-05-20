// var inputFields = document.querySelectorAll('input')
var pencils = document.querySelectorAll('i')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
var oldValuesDetail = {}
var oldValuesTimeFrames = {}
const commentInput = document.getElementById('comment-input')

executeFunctions()

function executeFunctions() {  // REVIEW: tên hàm không rõ nghĩa, VD có thể đặt là initScreen() -> "khởi tạo màn hình"
    addEventInput()
    changeSelectTag()
    sendData()
    setEventForStars()
    setUserStarRating()
    getAverageUsersRating()
}

for (let i = 1; i < stadiumFormDetail.length; i++) {
    oldValuesDetail[stadiumFormDetail[i].id] = stadiumFormDetail[i].value
}

for (let i = 1; i < stadiumFormTimeFrames.length; i++) {
    if ( stadiumFormTimeFrames[i].checked || !stadiumFormTimeFrames[i].checked ) {
        oldValuesTimeFrames[stadiumFormTimeFrames[i].id] = stadiumFormTimeFrames[i].checked
    }else{  // REVIEW: thêm dấu cách giữa 2 đầu chữ "else"
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

for (let i = 0; i < pencils.length;i++) {  // REVIEW: thêm dấu cách sau dấu chấm phẩy
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
    // REVIEW: tương tự review code python: không nên dùng kiểu dữ liệu để đặt tên biến
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

        e.preventDefault()  // REVIEW: những hàm như e.preventDefault, e.stopPropagation nên cho lên đầu
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
                let totalOfStarTypeRated = data.total_of_star_type_rated
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

    // REVIEW: để loop qua các phần tử của "allUsersStarRating" thì có thể dùng:
    // for (const userStarRating of allUsersStarRating) {
    //     ...
    // }
    // Hoặc
    // allUsersStarRating.forEach(function (userStarRating) {
    //     ...
    // })
    // Còn kiểu chú dùng giờ lạc hậu rồi, hơi khó đọc
    for (let i = 0; i < allUsersStarRating.length; i++ ) {
        let userStarRating = allUsersStarRating[i]
        let childrenElements = userStarRating.children
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

function getAverageUsersRating() {
    let stadiumId = document.getElementById('stadium-id').value
    $.ajax({
        type: 'get',
        url: '/danh-gia/',
        data: {
            stadiumId: stadiumId
        },
        success: function(data) {
            let totalOfStarTypeRated = data.total_of_star_type_rated

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
        for (let i = 0; i < allStarRateBtns.length; i++) {
            let starRateBtn = allStarRateBtns[i]
            if (starRateBtn.id === star) {
                let typeOfStar = starRateBtn.getAttribute('star-type')
                starRateBtn.innerHTML = `${typeOfStar} sao (${totalStar})`
            }
        }
    }
}

function setEventForStarTypeBtn(data) {
    let amountOfStarRatingType = data.amount_of_star_rating_type
    let allStarRateTypeBtns = document.querySelectorAll('.star-rate-btn')

    for (let i = 0; i < allStarRateTypeBtns.length; i++) {
        let starRateTypeBtn = allStarRateTypeBtns[i]

        starRateTypeBtn.addEventListener('click', function() {
            let starRateTypeBtnId = starRateTypeBtn.id
            var allCommentsDiv = document.getElementById('all-comments')
            allCommentsDiv.innerHTML = ''

            for (const [starType, allUsersRated] of Object.entries(amountOfStarRatingType)) {

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

