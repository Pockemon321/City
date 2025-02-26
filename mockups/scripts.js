// Анимация карточек с проблемами
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.request-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
});

// Валидация форм
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });

    return isValid;
}

// Обработка загрузки изображений
function handleImageUpload(input) {
    const file = input.files[0];
    const preview = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

// Фильтрация заявок
function filterRequests(status) {
    const cards = document.querySelectorAll('.request-card');
    
    cards.forEach(card => {
        const cardStatus = card.querySelector('.request-status').classList;
        if (status === 'all' || cardStatus.contains(`status-${status}`)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
