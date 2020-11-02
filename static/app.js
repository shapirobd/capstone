$('.bookmark-btn-form').each(function() {
    let form = $(this)[0]
    let card_id = form.id
    $(form).on('submit', async function(evt) {
        evt.preventDefault()
        if ($(form).hasClass('bookmark-form')) {
            axios.post(`/cards/${form.id}/bookmark`, {
                'card_id': card_id
            })
        
            $(form).empty()
            $(form).attr('action', `/cards/${card_id}/unbookmark`);
            $(form).removeClass('bookmark-form')
            $(form).addClass('unbookmark-form')
            $(form).append(`<button class="col btn btn-md btn-primary rounded-circle"><i class="fas fa-bookmark"></i></button>`)
        } else if ($(form).hasClass('unbookmark-form')) {
            axios.post(`/cards/${form.id}/unbookmark`, {
                'card_id': card_id
            })
        
            $(form).empty()
            $(form).attr('action', `/cards/${card_id}/bookmark`);
            $(form).removeClass('unbookmark-form')
            $(form).addClass('bookmark-form')
            $(form).append(`<button class="col btn btn-md btn-primary rounded-circle"><i class="far fa-bookmark"></i></button>`)
        }
    })
})

$('.friend-btn-form').each(function() {
    let form = $(this)[0]
    let username = form.id
    $(form).on('submit', async function(evt) {
        evt.preventDefault()
        if ($(form).hasClass('add-friend-form')) {
            axios.post(`/add_friend/${username}`, {
                'username': username
            })
        
            $(form).empty()
            $(form).attr('action', `/remove_friend/${username}`);
            $(form).removeClass('add-friend-form')
            $(form).addClass('remove-friend-form')
            $(form).append(`<button class="btn btn-sm btn-danger col my-1">Remove Friend</button>`)
        } else if ($(form).hasClass('remove-friend-form')) {
            axios.post(`/remove_friend/${username}`, {
                'username': username
            })
        
            $(form).empty()
            $(form).attr('action', `/add_friend/${username}`);
            $(form).removeClass('remove-friend-form')
            $(form).addClass('add-friend-form')
            $(form).append(`<button class="btn btn-sm btn-primary col my-1">Add Friend</button>`)
        }
    })
})

$('.add-to-deck-btn').each(function() {
    let btn = $(this)[0]
    $(btn).on('click', function(evt) {
        evt.preventDefault()
        toggleDropdownIcon(btn)
    })
})

$('.show-info-btn').each(function() {
    let btn = $(this)[0]
    $(btn).on('click', function(evt) {
        evt.preventDefault()
        toggleDropdownIcon(btn)
    })
})

function toggleDropdownIcon(btn) {
    if ($(btn).hasClass('unselected')) {
        let logo = $(btn).find('i')
        $(btn).removeClass('unselected')
        $(btn).addClass('selected')
        $(logo).replaceWith('<i class="fas fa-caret-down"></i>')
    } else if ($(btn).hasClass('selected')) {
        let logo = $(btn).find('i')
        $(btn).removeClass('selected')
        $(btn).addClass('unselected')
        $(logo).replaceWith('<i class="fas fa-caret-left"></i>')
    }
}

$('.delete-from-deck-btn').each(function() {
    let btn = $(this)[0]
    $(btn).on('click', async function(evt) {
        evt.preventDefault()
        let idSplit = $(btn).attr('id').split('-')
        let deckId = idSplit[0]
        let cardId = idSplit[1]

        await axios.post(`/cards/${cardId}/decks/${deckId}/delete`)
        $(`#card-${cardId}-col`).remove()
    })
})

$('.delete-from-friends-btn').each(function() {
    let btn = $(this)[0]
    $(btn).on('click', async function(evt) {
        evt.preventDefault()
        let friendUsername = $(btn).attr('id')

        await axios.post(`/remove_friend/${friendUsername}`)
        $(`#friend-${friendUsername}-col`).remove()
    })
})

$('.deck-btn').each(function() {
    let btn = $(this)[0]
    $(btn).on('click', async function(evt) {
        evt.preventDefault()
        let idSplit = $(btn).attr('id').split('-')
        let cardId = idSplit[0]
        let deckId = idSplit[1]

        await axios.post(`/cards/${cardId}/decks/${deckId}`)
        let dropdownMenu = $(`#add-${cardId}`)
        dropdownMenu.removeClass('show')
        let dropdownBtn = $(`#add-${cardId}-btn`)
        toggleDropdownIcon(dropdownBtn)
    })
})