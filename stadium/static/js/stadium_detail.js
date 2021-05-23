
var stadiumFormTimeFrames = document.querySelector('.stadium-form-time-frames').querySelectorAll('input')
var stadiumFormDetail = document.querySelector('.stadium-form-detail').querySelectorAll('input')
var oldValuesTimeFrames = getStadiumTimeFramesInformation()
var oldValuesDetail =  getStadiumInformation()
var modalEditForm = new bootstrap.Modal(document.getElementById('edit-rate-form-modal'))

initScreen()

function initScreen() { 
    setEventForPencilsIcon()
    addEventInput()
    changeSelectTag()
    sendData()
    setEventForStars()
    setUserStarRating()
    getAverageUsersRating()
    editUserRated()
    
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
    try {
        var spanChildrens = document.getElementById('star-rating').children
        const oneStar = document.getElementById('one-star')
        const twoStar = document.getElementById('two-star')
        const threeStar = document.getElementById('three-star')
        const fourStar = document.getElementById('four-star')
        const fiveStar = document.getElementById('five-star')
        const starType = [oneStar, twoStar, threeStar, fourStar, fiveStar]

        const oneStarId = oneStar.id
        const twoStarId = twoStar.id
        const threeStarId = threeStar.id
        const fourStarId = fourStar.id
        const fiveStarId = fiveStar.id

        setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
        
    } catch(error) {
        console.log(error)
    }
}

function setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId) {
    starType.forEach(item => {
        item.addEventListener('click', function(e) {
            handleStarSelect(e.target.id, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
        })
    });
}

function handleStarSelect(starId, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId) {
    switch(starId) {
        case oneStarId: {
            addOrRemoveCheckedClass(1, spanChildrens)
            return
        }
        case twoStarId: {
            addOrRemoveCheckedClass(2, spanChildrens)
            return
        }
        case threeStarId: {
            addOrRemoveCheckedClass(3, spanChildrens)
            return
        }
        case fourStarId: {
            addOrRemoveCheckedClass(4, spanChildrens)
            return
        }
        case fiveStarId: {
            addOrRemoveCheckedClass(5, spanChildrens)
            return
        }
    }
}

function addOrRemoveCheckedClass(size, spanChildrens) {
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
    let stadiumId = document.getElementById('stadium-id').value

    try {
        let commentBtn = document.getElementById('comment-btn')
        commentBtn.addEventListener('click', (e) => {
            e.preventDefault() 

            let spanChildrens = document.getElementById('star-rating').children
            spanChildrens = [].slice.call(spanChildrens, 0).reverse()

            let starPoint = getStarsPoint(spanChildrens)
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
                    let allCommentsDiv = document.getElementById('all-comments')

                    handleDataRespone(data, allCommentsDiv)
                    // clearInputAndStar(commentContent)
                    getTotalOfStarType(totalOfStarTypeRated)
                    setEventForStarTypeBtn(data, allCommentsDiv)
                },
                error: (error) => {
                    console.log(error)
                }
            })
        })
    } catch(error) {
        console.log(error)
    }
    
}

function getStarsPoint(spanChildrens) {
    let starPoint = 0
    for (let item of spanChildrens) {
        itemPoint = item.getAttribute('point')
        if (itemPoint > 0) {
            starPoint = itemPoint
        }
    }

    if (starPoint === 0) {
        starPoint = 5
    }
    return starPoint
}

function handleDataRespone(data, allCommentsDiv) {
    let userRated = data.user_rated_information

    createElementForUserRated(userRated, allCommentsDiv)
    checkUserRatePermission(userRated)
}

function checkUserRatePermission(userRated) {
    let userRatePermission = userRated.user_rate_permission
    let stadiumRate = document.getElementById('stadium-rate')

    if (userRatePermission === false) {
        stadiumRate.innerHTML = '<h3>Bạn đã hết lượt đánh giá</h3>'
    }
}

function setUserStarRating() {
    let allUsersStarRating = document.querySelectorAll('.user-star-rating')

    for (let userStarRating of allUsersStarRating ) {
        let childrenElements = userStarRating.children
        let userStarPointRated = childrenElements[childrenElements.length - 1].value
        childrenElements = Array.from(childrenElements);

        for (let [index, childrenElement] of childrenElements.entries()) {
            if (index < userStarPointRated) {
                if (childrenElement.classList.contains('checked') === false) {
                    childrenElement.classList.add('checked')
                }
            } else {
                if (childrenElement.classList.contains('checked')) {
                    childrenElement.classList.remove('checked')
                }
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
    let allCommentsDiv = document.getElementById('all-comments')
    $.ajax({
        type: 'get',
        url: '/danh-gia/',
        data: {
            stadiumId: stadiumId
        },
        success: function(data) {
            getTotalOfStarType(data)
            setEventForStarTypeBtn(data, allCommentsDiv)
            getUsersRated(data, allCommentsDiv) 
        },
        error: function(error) {
            console.log(error)
        }
    })
}

function getTotalOfStarType(data) {
    let totalOfStarTypeRated = data.stars_type_rated_numbers
    console.log('totalOfStarTypeRated', totalOfStarTypeRated)
    let starRateBtns = document.querySelectorAll('.star-rate-btn')

    
    for (let starRateBtn of starRateBtns) {
        let typeOfStar = starRateBtn.getAttribute('star-type')
        starRateBtn.innerHTML = `${typeOfStar} sao`

        if (typeOfStar === null) {
            starRateBtn.innerHTML = 'Tất cả'
        } 
        for (const [star, totalStar] of Object.entries(totalOfStarTypeRated)) {
            if (starRateBtn.id === star) {
                if (totalStar > 0) {
                    console.log(totalStar)
                    starRateBtn.innerHTML = `${typeOfStar} sao (${totalStar})`
                } else {
                    starRateBtn.innerHTML = `${typeOfStar} sao`
                } 
            }
        }   
    }
}

function setEventForStarTypeBtn(data, allCommentsDiv) {
    let summaryOfStarsType = data.summary_of_stars_type
    let allStarRateTypeBtns = document.querySelectorAll('.star-rate-btn')
    console.log("asef", summaryOfStarsType)
    for (let starRateTypeBtn of allStarRateTypeBtns) {
        starRateTypeBtn.addEventListener('click', function() {
            let starRateTypeBtnId = starRateTypeBtn.id
            allCommentsDiv.innerHTML = ''

            for (const [starType, allUsersRated] of Object.entries(summaryOfStarsType)) {

                if (starType === starRateTypeBtnId) {
                    console.log(starType)
                    for (let userRated of allUsersRated) {
                        createElementForUserRated(userRated, allCommentsDiv)
                    }
                    showEditModal()
                }
            }
        })
    }
}

function getUsersRated(data, allCommentsDiv) {
    let usersRated = data.summary_of_stars_type.users_rated

    for (userRated of usersRated) {
        createElementForUserRated(userRated, allCommentsDiv)
    }
    showEditModal()
}

function createElementForUserRated(userRated, allCommentsDiv) {
    let currentUserId = document.getElementById('user-id').value
    let username = userRated.username
    let userRatedId = userRated.user_id
    let commentContent = userRated.comment
    let star_point = userRated.star_point
    let commentDiv = document.createElement('div')
    let aTag = document.createElement('a')
    let h4Tag = document.createElement('h4')
    let userStarRatingDiv = document.createElement('div')
    let starPointInput = document.createElement('input')
    let hrTag = document.createElement('hr')
    let iTag = document.createElement('i')

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
    aTag.classList.add('username') 

    h4Tag.className = 'user-comment'

    iTag.id = 'edit-rate'
    iTag.className = 'fas fa-edit'
    iTag.setAttribute('point', star_point)
    iTag.setAttribute('comment', commentContent)

    starPointInput.type = 'hidden'
    starPointInput.id = 'user-star-point-rating'
    starPointInput.className = 'user-star-point-rating'
    starPointInput.value = star_point


    aTag.innerHTML = username
    h4Tag.innerHTML = commentContent

    userStarRatingDiv.appendChild(starPointInput)
    commentDiv.appendChild(aTag)

    if (currentUserId == userRatedId) {
        commentDiv.id = 'user-rated'
        iTag.setAttribute('userRated', 'user-rated')

        commentDiv.appendChild(iTag)
    }

    commentDiv.appendChild(h4Tag)
    commentDiv.appendChild(userStarRatingDiv)
    allCommentsDiv.appendChild(commentDiv)
    allCommentsDiv.appendChild(hrTag)
    setUserStarRating()
    // showEditModal()
}

function editUserRated() {
    let commentContent = document.getElementById('comment-input')
    let csrf = document.getElementsByName('csrfmiddlewaretoken')
    let stadiumId = document.getElementById('stadium-id').value
    let spanChildrens = document.getElementById('star-rated').children
    let editCommentBtn = document.getElementById('edit-comment-btn')
    let allCommentsDiv = document.getElementById('all-comments')
    
    spanChildrens = Array.from(spanChildrens).reverse()

    editCommentBtn.addEventListener('click', function(e) {
        e.preventDefault()

        let starPoint = getStarsPoint(spanChildrens)
        let editRatedIcon = document.getElementById('edit-rate')
        let commentInforId = editRatedIcon.getAttribute('userRated')
        let commentInfor = document.getElementById(commentInforId)
        let userComment = commentInfor.getElementsByClassName('user-comment')[0]
        let userStarRated = commentInfor.getElementsByClassName('user-star-rating')[0]
        let userStarPointRated = userStarRated.getElementsByClassName('user-star-point-rating')[0]

        $.ajax({
            type: 'post',
            url: '/sua-danh-gia/',
            data: {
                commentData: commentContent.value,
                starPoint: starPoint,
                stadiumId: stadiumId,
                csrfmiddlewaretoken: csrf[0].value
            },
            success: function(data) {
                let userRated = data.user_rated_information_edited
                let userPointEdited = userRated.star_point
                let userCommentEdited = userRated.comment

                userComment.innerHTML = userCommentEdited
                userStarPointRated.value = userPointEdited

                editRatedIcon.setAttribute('point', userPointEdited) 
                editRatedIcon.setAttribute('comment', userCommentEdited)

                setUserStarRating()
                setEventForStarTypeBtn(data, allCommentsDiv)
                getTotalOfStarType(data) 
                modalEditForm.hide()
            }   
        })
        
    })
}

function showEditModal() {
    let editRatedIcon = document.getElementById('edit-rate')
    let spanChildrens = document.getElementById('star-rated').children

    const oneStar = document.getElementById('one-star-rated')
    const twoStar = document.getElementById('two-star-rated')
    const threeStar = document.getElementById('three-star-rated')
    const fourStar = document.getElementById('four-star-rated')
    const fiveStar = document.getElementById('five-star-rated')
    const starType = [oneStar, twoStar, threeStar, fourStar, fiveStar]

    const oneStarId = oneStar.id
    const twoStarId = twoStar.id
    const threeStarId = threeStar.id
    const fourStarId = fourStar.id
    const fiveStarId = fiveStar.id
    
    setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
    spanChildrens = Array.from(spanChildrens).reverse()
    
    editRatedIcon.addEventListener('click', function(e) {
        let starPoint = e.target.getAttribute('point')
        let commentContent = e.target.getAttribute('comment')
        let commentInput = document.getElementById('comment-input')

        commentInput.value = commentContent
        
        for (const [index, spanChildren] of spanChildrens.entries()) {
            if (index < starPoint) {
                spanChildren.classList.add('checked')
            } else {
                spanChildren.classList.remove('checked')
            }
        }

        modalEditForm.show()
    })
}