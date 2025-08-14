 document.addEventListener('DOMContentLoaded', function() {
            // Search functionality
            const searchInput = document.getElementById('searchInput');
            const tableBody = document.getElementById('studentsTableBody');
            const rows = tableBody.querySelectorAll('tr');

            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();

                rows.forEach(row => {
                    const studentName = row.querySelector('.student-name').textContent.toLowerCase();
                    const category = row.querySelector('.category').textContent.toLowerCase();

                    if (studentName.includes(searchTerm) || category.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            });

            // Select all checkbox functionality
            const selectAllCheckbox = document.getElementById('selectAll');
            const rowCheckboxes = document.querySelectorAll('.row-checkbox');

            selectAllCheckbox.addEventListener('change', function() {
                rowCheckboxes.forEach(checkbox => {
                    checkbox.checked = this.checked;
                });
            });

            // Individual checkbox functionality
            rowCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', function() {
                    const checkedBoxes = document.querySelectorAll('.row-checkbox:checked');
                    selectAllCheckbox.checked = checkedBoxes.length === rowCheckboxes.length;
                    selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < rowCheckboxes.length;
                });
            });

            // Action button functionality
       
                if (e.target.classList.contains('reminder-btn') || e.target.closest('.reminder-btn')) {
                    const row = e.target.closest('tr');
                    const studentName = row.querySelector('.student-name').textContent;
                    alert(`Sending reminder to ${studentName}`);
                }

                if (e.target.classList.contains('message-btn') || e.target.closest('.message-btn')) {
                    const row = e.target.closest('tr');
                    const studentName = row.querySelector('.student-name').textContent;
                    alert(`Opening message for ${studentName}`);
                }
            });

            // Export CSV functionality
            const exportBtn = document.querySelector('.export-btn');
            exportBtn.addEventListener('click', function() {
                const data = [];
                const headers = ['Student Name', 'Age Group', 'Category', 'Status', 'Registration Date'];
                data.push(headers.join(','));

                rows.forEach(row => {
                    if (row.style.display !== 'none') {
                        const cells = [
                            row.querySelector('.student-name').textContent,
                            row.cells[2].textContent,
                            row.querySelector('.category').textContent,
                            row.querySelector('.status').textContent,
                            row.cells[5].textContent
                        ];
                        data.push(cells.join(','));
                    }
                });

                const csvContent = data.join('\n');
                const blob = new Blob([csvContent], {
                    type: 'text/csv'
                });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'students_data.csv';
                a.click();
                window.URL.revokeObjectURL(url);
            });

            // Filter button functionality
            const filterBtn = document.querySelector('.filter-btn');
            filterBtn.addEventListener('click', function() {
                const filterOptions = ['All', 'Enrolled', 'Not Started', 'Registered'];
                const selectedFilter = prompt('Filter by status:\n' + filterOptions.join('\n'));

                if (selectedFilter && selectedFilter !== 'All') {
                    rows.forEach(row => {
                        const status = row.querySelector('.status').textContent;
                        if (status.toLowerCase().includes(selectedFilter.toLowerCase())) {
                            row.style.display = '';
                        } else {
                            row.style.display = 'none';
                        }
                    });
                } else if (selectedFilter === 'All') {
                    rows.forEach(row => {
                        row.style.display = '';
                    });
                }
            });
        });