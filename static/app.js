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
// $('.bookmark-form').on('submit', async function(evt) {
//     evt.preventDefault()
    
//     axios.post(`/cards/${form.id}/bookmark`, {
//         'card_id': card_id
//     })

//     $(form).empty()
//     $(form).attr('action', `/cards/${card_id}/unbookmark`);
//     $(form).removeClass('bookmark-form')
//     $(form).addClass('unbookmark-form')
//     $(form).append(`<button class="col btn btn-md btn-primary"><i class="fas fa-bookmark"></i></button>`)
// })

// $('.unbookmark-form').on('submit', async function(evt) {
//     evt.preventDefault()
//     let form = $(this)[0]
//     let card_id = form.id
//     axios.post(`/cards/${form.id}/unbookmark`, {
//         'card_id': card_id
//     })

//     $(form).empty()
//     $(form).attr('action', `/cards/${card_id}/bookmark`);
//     $(form).removeClass('unbookmark-form')
//     $(form).addClass('bookmark-form')
//     $(form).append(`<button class="col btn btn-md btn-primary"><i class="far fa-bookmark"></i></button>`)})