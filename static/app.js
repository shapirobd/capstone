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
            $(form).append(`<button class="col btn btn-md btn-primary"><i class="fas fa-bookmark"></i></button>`)
        } else if ($(form).hasClass('unbookmark-form')) {
            axios.post(`/cards/${form.id}/unbookmark`, {
                'card_id': card_id
            })
        
            $(form).empty()
            $(form).attr('action', `/cards/${card_id}/bookmark`);
            $(form).removeClass('unbookmark-form')
            $(form).addClass('bookmark-form')
            $(form).append(`<button class="col btn btn-md btn-primary"><i class="far fa-bookmark"></i></button>`)
        }
    })
})

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