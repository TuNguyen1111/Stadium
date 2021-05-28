var stadiumFormTimeFrames = $('form#stadium-form-time-frames input')
var stadiumFormDetail = $('#stadium-form-detail input')
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
    // editUserRated()
}

// AJAX REQUEST
function sendData() {
    let commentContent = $('#comment-input')
    console.log(commentContent)
    let csrf = $('input[name=csrfmiddlewaretoken]').val()
    let stadiumId = $('#stadium-id').val()

    try {
        $('#comment-btn').click( (e) => {
            e.preventDefault() 
            let spanChildrens = $('#star-rating').children().toArray().reverse()
            let starPoint = getStarsPoint(spanChildrens)

            $.ajax({
                type: 'post',
                url: '/danh-gia/',
                data: {
                    commentData: commentContent.val(),
                    starPoint: starPoint,
                    stadiumId: stadiumId,
                    csrfmiddlewaretoken: csrf
                },
                success: (data) => {
                    let allCommentsDiv = $('#all-comments')

                    handleDataRespone(data, allCommentsDiv)
                    // clearInputAndStar(commentContent)
                    getTotalOfStarType(data)
                    setEventForStarTypeBtn(data, allCommentsDiv)
                    showEditModal()
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

function getAverageUsersRating() {
    let stadiumId = $('#stadium-id').val()
    let allCommentsDiv = $('#all-comments')
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

// FUNCTIONS
function getInput() {
    let getData = $(this).attr('data-name')
    let dataCheck = $(this).attr('data-check')
    let checkBox = $(`#${dataCheck}`)
    let input = $(`#${getData}`)
    
    if (input.attr('disabled')) {
        input.attr('disabled', false)
    } else {
        input.attr('disabled', true)
    }

    if (checkBox) {
        if (checkBox.attr('disabled')) {
            checkBox.attr('disabled', false)
        } else {
            checkBox.attr('disabled', true)
        }
    }
}

function setEventForPencilsIcon() {
    $('i').each((index, pencil) => {
        $(pencil).click(getInput)
    })
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

function checkValueOfDetailInput(e) {
    let currentValue = $(e.target).val()
    let saveBtn = $('#saveDetailBtn')
    
    if (currentValue != oldValuesDetail[$(e.target).attr('id')]) {
        saveBtn.attr('disabled', false)
        stadiumFormDetail.attr('disabled', false)
    } else {
        saveBtn.attr('disabled', true)
    }
}

function checkValueOfTimeFrameInput(e) {
    let currentValue = $(e.target).val()
    let checkedValue = $(e.target).attr('checked')
    let saveBtn = $('#saveTimeFramesBtn')

    if (checkedValue) {
        currentValue = checkedValue
    }

    if (currentValue != oldValuesTimeFrames[$(e.target).attr('id')]) {
        saveBtn.attr('disabled', false)
        
        stadiumFormTimeFrames.attr('disabled', false)
    } else {
        saveBtn.attr('disabled', true)
    }
}

function addEventInput() {
    stadiumFormDetail.on('input', checkValueOfDetailInput)
    stadiumFormTimeFrames.on('input', checkValueOfTimeFrameInput)
    stadiumFormTimeFrames.attr('disabled', true)
}

function turnOnDeleteModal() {
    $('#delete-form-modal').modal('show')
}

function tunrOndeleteTimeFrameModal(id) {
    $(`#delete-timeframe-${id}`).modal('show')
}

function changeSelectTag() {
    let inputTags = $('select')
    for (let item of inputTags) {
        let value = item.options[item.selectedIndex].text;
        let pTag = $(`<p>${value}</p>`)
        $(item).replaceWith(pTag)
    }
}

function setEventForStars() {
    try {
        var spanChildrens = $('#star-rating').children()
        const oneStar = $('#one-star')
        const twoStar = $('#two-star')
        const threeStar = $('#three-star')
        const fourStar = $('#four-star')
        const fiveStar = $('#five-star')
        const starType = [oneStar, twoStar, threeStar, fourStar, fiveStar]
    
        const oneStarId = oneStar.attr('id')
        const twoStarId = twoStar.attr('id')
        const threeStarId = threeStar.attr('id')
        const fourStarId = fourStar.attr('id')
        const fiveStarId = fiveStar.attr('id')

        setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
        
    } catch(error) {
        console.log(error)
    }
}

function setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId) {
    starType.forEach((item) => {
        item.on('click', function(e) {
            handleStarSelect(e.target.id, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
        })
    })
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
    spanChildrens = spanChildrens.toArray().reverse()
    
    for (let [index, children] of spanChildrens.entries()) {
        let childrenItem = $(children)
        if (index < size) {
            childrenItem.addClass('checked')
            childrenItem.attr('point', index + 1)
        } else {
            childrenItem.removeClass('checked')
            childrenItem.attr('point', 0)
        }
    }
}

function getStarsPoint(spanChildrens) {
    let starPoint = 0

    for (let item of spanChildrens) {
        itemPoint = $(item).attr('point')
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
    let noRatedTitle = $('#no-rated-title')
    
    if (noRatedTitle.length) {
        noRatedTitle.html('')
    }

    createElementForUserRated(userRated, allCommentsDiv)
    checkUserRatePermission(userRated)
}

function checkUserRatePermission(userRated) {
    let userRatePermission = userRated.user_rate_permission
    let stadiumRate = $('#stadium-rate')

    if (userRatePermission === false) {
        stadiumRate.html('<h3 class="notification-title">Bạn đã hết lượt đánh giá!</h3>')
    }
}

function setUserStarRating() {
    let usersStarRating = $('.user-star-rating')

    for (userStarRating of usersStarRating) {
        let childrenElements = $(userStarRating).children().toArray()
        let userStarPointRated = $(childrenElements[childrenElements.length - 1]).val()

        for (let [childrenPoint, childrenElement] of childrenElements.entries()) {
            if (childrenPoint < userStarPointRated) {
                $(childrenElement).addClass('checked')
            } else {
                $(childrenElement).removeClass('checked')
            }
        }
    }  
}

function clearInputAndStar(commentContent) {
    let starRatingInput = $('#star-rating')
    let childrenElements = starRatingInput.children().toArray()

    childrenElements.forEach( (childrenElement) => {
        $(childrenElement).removeClass('checked')
    })

    commentContent.val('')
}


function getTotalOfStarType(data) {
    let totalOfStarTypeRated = data.stars_type_rated_numbers
    let starRateBtns = $('.star-rate-btn')

    for (let starRateBtn of starRateBtns) {
        let starType = $(starRateBtn).attr('star-type')
        $(starRateBtn).text(`${starType} sao`)

        if (starType === undefined) {
            $(starRateBtn).text('Tất cả')
        }

        for (const [star, totalStar] of Object.entries(totalOfStarTypeRated)) {
            if ($(starRateBtn).attr('id') === star) {
                if (totalStar > 0) {
                    $(starRateBtn).text(`${starType} sao (${totalStar})`)
                } else {
                    $(starRateBtn).text(`${starType} sao`)
                }
            }
        }
    }
}

function setEventForStarTypeBtn(data, allCommentsDiv) {
    let summaryOfStarsType = data.summary_of_stars_type

    $('.star-rate-btn').on('click', function(e) {
        let currentBtn = $(e.target)
        let starRateTypeBtnId = currentBtn.attr('id')
        allCommentsDiv.html('')

        for (const [starType, usersRated] of Object.entries(summaryOfStarsType)) {
            if (starType === starRateTypeBtnId) {
                for (let userRated of usersRated) {
                    createElementForUserRated(userRated, allCommentsDiv)
                }
                showEditModal()
            }
        } 
    })
}

function getUsersRated(data, allCommentsDiv) {
    let usersRated = data.summary_of_stars_type.users_rated
    
    if(usersRated.length) {
        for (userRated of usersRated) {
            createElementForUserRated(userRated, allCommentsDiv)
        }
        showEditModal()
    } else {
        allCommentsDiv.html('<h3 id="no-rated-title">Hiện tại chưa có lượt đánh giá nào!</h3>')
    }
}

function createElementForUserRated(userRated, allCommentsDiv) {
    let currentUserId = $('#user-id').val()
    let username = userRated.username
    let userRatedId = userRated.user_id
    let commentContent = userRated.comment
    let starPoint = userRated.star_point

    let commentDiv = $('<div class="comment-infor"> </div>')
    let aTag = $(`<a class="mr-2 username">${username}</a>`)
    let h4Tag = $(`<h4 class="user-comment">${commentContent}</h4>`)
    let userStarRatingDiv = $('<div class="user-star-rating"></div>')
    let starPointInput = $(`<input type="hidden" class="user-star-point-rating" value="${starPoint}"/>`)
    let hrTag = $('<hr>')
    let iTag = $(`<i id="edit-rate" class="fas fa-edit" point="${starPoint}" comment="${commentContent}"></i>`)

    for (let i = 0; i < 5; i++) {
        let spanTag = $(`<span class="fa fa-star" id="user-${i + 1}-star"></span>`)
        userStarRatingDiv.append(spanTag)
    }

    commentDiv.append(aTag)
    if (currentUserId == userRatedId) {
        commentDiv.attr('id', 'current-user-rated')
        iTag.attr('userRated', 'current-user-rated')
        h4Tag.attr('id','current-user-comment')
        userStarRatingDiv.attr('id', 'current-user-star-rating')
        starPointInput.attr('id', 'current-user-star-point-rated')
        commentDiv.append(iTag)
    }

    userStarRatingDiv.append(starPointInput)
    commentDiv.append(h4Tag, userStarRatingDiv)
    allCommentsDiv.append(commentDiv, hrTag)
    allCommentsDiv.append(hrTag)
    setUserStarRating()
}

function editUserRated() {
    
    let commentContent = $('#comment-input')
    let csrf = $('input[name=csrfmiddlewaretoken]').val()
    let stadiumId = $('#stadium-id').val()
    let spanChildrens = $('#star-rated').children().toArray().reverse()
    let editCommentBtn = $('#edit-comment-btn')
    let allCommentsDiv = $('#all-comments')
    
    editCommentBtn.on('click', function(e) {
        e.preventDefault()

        let starPoint = getStarsPoint(spanChildrens)
        let editRatedIcon = $('#edit-rate')
        let commentInforId = editRatedIcon.attr('userRated')
        let commentInfor = $(`#${commentInforId}`)
        let userComment = commentInfor.children('#current-user-comment')
        let userStarRated = commentInfor.children('#current-user-star-rating')
        let userStarPointRated = userStarRated.children('#current-user-star-point-rated')

        $.ajax({
            type: 'post',
            url: '/sua-danh-gia/',
            data: {
                commentData: commentContent.val(),
                starPoint: starPoint,
                stadiumId: stadiumId,
                csrfmiddlewaretoken: csrf
            },
            success: function(data) {
                let userRated = data.user_rated_information_edited
                let userPointEdited = userRated.star_point
                let userCommentEdited = userRated.comment

                userComment.html(userCommentEdited)
                userStarPointRated.val(userPointEdited)

                editRatedIcon.attr({
                    'point': userPointEdited,
                    'comment': userCommentEdited
                }) 

                setUserStarRating()
                setEventForStarTypeBtn(data, allCommentsDiv)
                getTotalOfStarType(data) 
                modalEditForm.hide()
            }   
        })
        
    })
}

function showEditModal() {
    let editRatedIcon = $('#edit-rate')
    let spanChildrens = $('#star-rated').children()

    const oneStar = $('#one-star-rated')
    const twoStar = $('#two-star-rated')
    const threeStar = $('#three-star-rated')
    const fourStar = $('#four-star-rated')
    const fiveStar = $('#five-star-rated')
    const starType = [oneStar, twoStar, threeStar, fourStar, fiveStar]

    const oneStarId = oneStar.attr('id')
    const twoStarId = twoStar.attr('id')
    const threeStarId = threeStar.attr('id')
    const fourStarId = fourStar.attr('id')
    const fiveStarId = fiveStar.attr('id')
    
    setEventForEachStar(starType, spanChildrens, oneStarId, twoStarId, threeStarId, fourStarId, fiveStarId)
    
    spanChildrens = spanChildrens.toArray().reverse()
    editRatedIcon.on('click', function(e) {
        let starPoint = $(e.target).attr('point')
        let commentContent = $(e.target).attr('comment')
        let commentInput = $('#comment-input')

        commentInput.val(commentContent)
        
        for (const [index, spanChildren] of spanChildrens.entries()) {
            if (index < starPoint) {
                $(spanChildren).addClass('checked')
            } else {
                $(spanChildren).removeClass('checked')
            }
        }
        editUserRated()
        modalEditForm.show()
    })
}