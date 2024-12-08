deleteButton();
completeIcon();
lineBreaks();
editModal();
learnMoreDropdown();
tableValues();
filterForms();
descriptionDropdown();


// Delete confirmation
function deleteButton() {
    let deleteBtn = document.querySelectorAll('.deleteBtn');
    let question = document.querySelectorAll('.question');
    let noBtn = document.querySelectorAll('.hideQuestion');
    let yesBtn = document.querySelectorAll('.confirmdelete');

    for (let i = 0; i < deleteBtn.length; i++) {
        deleteBtn[i].addEventListener('click', function() {
            question[i].style.display = 'block';
        });

        noBtn[i].addEventListener('click', function() {
            question[i].style.display = 'none';
        });

        yesBtn[i].addEventListener('click', function() {
            document.getElementById('deleteInput').value = yesBtn[i].getAttribute('task-delete');
            document.getElementById('deleteForm').submit();
        });
    }
}


// Complete icon hover effect
function completeIcon() {
    let complete = document.querySelectorAll('.complete-button');

    for (let i = 0; i < complete.length; i++) {
        complete[i].addEventListener('mouseover', function() {
            complete[i].classList.remove('bi-check-circle');
            complete[i].classList.add('bi-check-circle-fill');
        });

        complete[i].addEventListener('mouseout', function() {
            complete[i].classList.remove('bi-check-circle-fill');
            complete[i].classList.add('bi-check-circle');
        });

        complete[i].addEventListener('click', function() {
            document.getElementById('completeInput').value = complete[i].getAttribute('task-complete');
            document.getElementById('completeForm').submit();
        });
    }
}


// Edit modal
function editModal() {
    let editModalElement = document.getElementById('editTaskModal');
    if (!editModalElement) return;

    let editBtns = document.querySelectorAll('.editBtn');

    // Autofill modal
    for (let i = 0; i < editBtns.length; i++) {
        editBtns[i].addEventListener('click', function() {
            document.getElementById('editTaskId').value = editBtns[i].getAttribute('data-task-id');
            document.getElementById('editTaskTitle').value = editBtns[i].getAttribute('data-task-title');
            document.getElementById('editTaskDescription').value = editBtns[i].getAttribute('data-task-description');

            let taskDeadline = editBtns[i].getAttribute('data-task-deadline');
            if (taskDeadline) {
                let deadlineFormatted = taskDeadline.replace(' ', 'T');
                document.getElementById('editTaskDeadline').value = deadlineFormatted;
            } else {
                document.getElementById('editTaskDeadline').value = '';
            }

            document.querySelector('#errorMessage').innerHTML = '';
            new bootstrap.Modal(document.getElementById('editTaskModal')).show();
        });
    }

    // Check for missing fields
    document.getElementById('editTaskModal').addEventListener('submit', function(event) {
        let title = document.getElementById('editTaskTitle').value.trim();
        let description = document.getElementById('editTaskDescription').value.trim();
        let deadline = document.getElementById('editTaskDeadline').value;

        if (title === '') {
            document.querySelector('#errorMessage').innerHTML = 'Missing Title.';
            event.preventDefault();
            return;
        }

        if (description === '') {
            document.querySelector('#errorMessage').innerHTML = 'Missing Description.';
            event.preventDefault();
            return;
        }
    });
}


// Learn more dropdown
function learnMoreDropdown() {
    let dropdown = document.getElementById('dropdown');
    if (!dropdown) return;

    document.getElementById('dropdown').addEventListener('click', function() {
        let paragraph = document.getElementById('paragraph');
        let dropdownIcon = document.getElementById('dropdown-icon');

        if (paragraph.style.display === 'none') {
            paragraph.style.display = 'block';
            dropdownIcon.classList.remove('bi-caret-down-fill');
            dropdownIcon.classList.add('bi-caret-up-fill');
        } else {
            paragraph.style.display = 'none';
            dropdownIcon.classList.remove('bi-caret-up-fill');
            dropdownIcon.classList.add('bi-caret-down-fill');
        }
    });
}


// EPS table values coloring
function tableValues() {
    let values = document.querySelectorAll('.epsValues');

    for (let i = 0; i < values.length; i++) {
        if (values[i].innerHTML === '\u2013High') {
            values[i].style.color = 'green';
        }
        else if (values[i].innerHTML === '\u2013Medium') {
            values[i].style.color = '#fc9903';
        }
        else {
                values[i].style.color = 'red';
        }
    }
}


// Filter tasks form submission
function filterForms() {
    let options = document.querySelectorAll('.dropdown-item');

    for (let i = 0; i < options.length; i++) {
        options[i].addEventListener('click', function() {
            document.getElementById('filterOption').value = options[i].getAttribute('filter-option');
            document.getElementById('filterForm').submit();
        });
    }
}


// History description dropdown
function descriptionDropdown() {
    let tableDropdowns = document.querySelectorAll('.table-description');
    let tableDescriptions = document.querySelectorAll('.description-dropdown');
    let icons = document.querySelectorAll('.dropdown-icon-table');

    for (let i = 0; i < tableDropdowns.length; i++) {
        tableDropdowns[i].addEventListener('click', function() {

            if (tableDescriptions[i].style.display === 'none') {
                tableDescriptions[i].style.display = 'block';
                icons[i].classList.remove('bi-caret-down-fill');
                icons[i].classList.add('bi-caret-up-fill');
            } else {
                tableDescriptions[i].style.display = 'none';
                icons[i].classList.remove('bi-caret-up-fill');
                icons[i].classList.add('bi-caret-down-fill');
            }
        });
    }
}


// Place line breaks in history descriptions
function lineBreaks() {
    let descriptions = document.querySelectorAll(".cardDescription");

    for (let i = 0; i < descriptions.length; i++) {
        let content = descriptions[i].innerHTML;
        let cleaned_text = content.replace(/\n/g, '<br>');
        descriptions[i].innerHTML = cleaned_text;
    }
}
