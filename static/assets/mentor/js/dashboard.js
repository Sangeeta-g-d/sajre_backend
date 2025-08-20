// Universal Search and Filter Implementation
document.addEventListener('DOMContentLoaded', function() {
    // Get all table rows
    const tableRows = document.querySelectorAll('#studentsTableBody tr');
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const categoryFilter = document.getElementById('categoryFilter');
    const applyFiltersBtn = document.getElementById('applyFilters');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const filterDropdown = document.querySelector('.filter-content');
    const noResultsMessage = document.getElementById('noResultsMessage');
    const table = document.querySelector('.students-table');
    
    // Show/hide filter dropdown
    document.querySelector('.filter-btn').addEventListener('click', function() {
        filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
    });
    
    // Close filter dropdown when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.filter-dropdown')) {
            filterDropdown.style.display = 'none';
        }
    });
    
    // Function to filter table rows
    function filterTable() {
        const searchText = searchInput.value.toLowerCase();
        const statusValue = statusFilter.value;
        const categoryValue = categoryFilter.value;
        
        let visibleRows = 0;
        
        tableRows.forEach(row => {
            let showRow = true;
            
            // Search filter
            if (searchText) {
                const name = row.querySelector('.student-name').textContent.toLowerCase();
                const email = row.querySelector('.student-email').textContent.toLowerCase();
                const category = row.querySelector('.category').textContent.toLowerCase();
                
                if (!name.includes(searchText) && !email.includes(searchText) && !category.includes(searchText)) {
                    showRow = false;
                }
            }
            
            // Status filter
            if (showRow && statusValue !== 'all') {
                const status = row.querySelector('.status').classList.contains(statusValue);
                if (!status) {
                    showRow = false;
                }
            }
            
            // Category filter
            if (showRow && categoryValue !== 'all') {
                const categoryText = row.querySelector('.category').textContent;
                if (categoryText !== categoryValue) {
                    showRow = false;
                }
            }
            
            // Show or hide the row based on filters
            row.style.display = showRow ? '' : 'none';
            
            // Count visible rows
            if (showRow) {
                visibleRows++;
            }
        });
        
        // Show/hide no results message
        if (visibleRows === 0) {
            noResultsMessage.style.display = 'block';
            table.style.display = 'none';
        } else {
            noResultsMessage.style.display = 'none';
            table.style.display = 'table';
        }
    }
    
    // Event listeners for filtering
    searchInput.addEventListener('input', filterTable);
    applyFiltersBtn.addEventListener('click', function() {
        filterTable();
        filterDropdown.style.display = 'none';
    });
    
    // Reset filters
    resetFiltersBtn.addEventListener('click', function() {
        searchInput.value = '';
        statusFilter.value = 'all';
        categoryFilter.value = 'all';
        filterTable();
        filterDropdown.style.display = 'none';
    });
    
    // Universal Modal Script
    function initParticipantModal() {
        // Get all view buttons
        const viewButtons = document.querySelectorAll('.view-btn');
        
        // Add click event to each button
        viewButtons.forEach(button => {
            button.addEventListener('click', function() {
                const userId = this.getAttribute('data-user-id');
                
                // Fetch participant data via AJAX
                fetch(`/mentor/get-participant-details/${userId}/`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Update modal with participant data
                        document.getElementById('modalParticipantName').textContent = data.full_name || 'N/A';
                        document.getElementById('modalParticipantEmail').textContent = data.email || 'N/A';
                        document.getElementById('modalParticipantPhone').textContent = data.phone_number || 'N/A';
                        document.getElementById('modalParticipantPhoto').src = data.photo || 'https://via.placeholder.com/200';
                        
                        // Personal Info
                        document.getElementById('modalParticipantAge').textContent = data.age || 'N/A';
                        document.getElementById('modalParticipantDob').textContent = data.dob || 'N/A';
                        document.getElementById('modalParticipantFather').textContent = data.father_name || 'N/A';
                        document.getElementById('modalParticipantMother').textContent = data.mother_name || 'N/A';
                        
                        // Address Info
                        document.getElementById('modalParticipantAddress').textContent = data.full_address || 'N/A';
                        document.getElementById('modalParticipantCity').textContent = data.city || 'N/A';
                        document.getElementById('modalParticipantState').textContent = data.state || 'N/A';
                        document.getElementById('modalParticipantPincode').textContent = data.pincode || 'N/A';
                        
                        // Education Info
                        document.getElementById('modalParticipantSchool').textContent = data.school_name || data.university_name || 'N/A';
                        document.getElementById('modalParticipantGrade').textContent = data.grade || data.stream || 'N/A';
                        document.getElementById('modalParticipantBoard').textContent = data.school_board || data.university || 'N/A';
                        
                        // Registration Info
                        document.getElementById('modalParticipantCategory').textContent = data.category || 'N/A';
                        document.getElementById('modalParticipantStatus').textContent = data.has_paid ? 'Enrolled' : 'Not Enrolled';
                        document.getElementById('modalParticipantRegDate').textContent = data.registration_date || 'N/A';
                        document.getElementById('modalParticipantReferral').textContent = data.referral_code || 'N/A';
                    })
                    .catch(error => {
                        console.error('Error fetching participant details:', error);
                        alert('Error loading participant details. Please try again.');
                    });
            });
        });
    }
    
    // Initialize the modal functionality
    initParticipantModal();
    
    // Reinitialize modal when table is filtered (in case new rows are added dynamically)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                initParticipantModal();
            }
        });
    });
    
    observer.observe(document.getElementById('studentsTableBody'), {
        childList: true,
        subtree: true
    });
});document.addEventListener('DOMContentLoaded', function() {
    // Get all table rows
    const tableRows = document.querySelectorAll('#studentsTableBody tr');
    const searchInput    = document.getElementById('searchInput');
    const statusFilter   = document.getElementById('statusFilter');
    const categoryFilter = document.getElementById('categoryFilter');
    const applyFiltersBtn = document.getElementById('applyFilters');
    const resetFiltersBtn = document.getElementById('resetFilters');
    const filterDropdown  = document.querySelector('.filter-content');
    const filterBtn       = document.querySelector('.filter-btn');  // <-- added variable
    const noResultsMessage = document.getElementById('noResultsMessage');
    const table = document.querySelector('.students-table');

    // Handle filter dropdown only if filter button actually exists on the page
    if (filterBtn && filterDropdown) {
        // Show/hide filter dropdown
        filterBtn.addEventListener('click', function() {
            filterDropdown.style.display = filterDropdown.style.display === 'block' ? 'none' : 'block';
        });
        
        // Close filter dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.filter-dropdown')) {
                filterDropdown.style.display = 'none';
            }
        });
    }

    // Function to filter table rows
    function filterTable() {
        const searchText    = searchInput.value.toLowerCase();
        const statusValue   = statusFilter ? statusFilter.value : 'all';
        const categoryValue = categoryFilter ? categoryFilter.value : 'all';
        
        let visibleRows = 0;
        
        tableRows.forEach(row => {
            let showRow = true;
            
            // Search filter
            if (searchText) {
                const name     = row.querySelector('.student-name').textContent.toLowerCase();
                const email    = row.querySelector('.student-email').textContent.toLowerCase();
                const category = row.querySelector('.category') ? row.querySelector('.category').textContent.toLowerCase() : '';
                
                if (!name.includes(searchText) && !email.includes(searchText) && !category.includes(searchText)) {
                    showRow = false;
                }
            }
            
            // Status filter
            if (showRow && statusFilter && statusValue !== 'all') {
                const status = row.querySelector('.status').classList.contains(statusValue);
                if (!status) {
                    showRow = false;
                }
            }
            
            // Category filter
            if (showRow && categoryFilter && categoryValue !== 'all') {
                const categoryText = row.querySelector('.category') ? row.querySelector('.category').textContent : '';
                if (categoryText !== categoryValue) {
                    showRow = false;
                }
            }
            
            // Show or hide the row based on filters
            row.style.display = showRow ? '' : 'none';
            
            // Count visible rows
            if (showRow) {
                visibleRows++;
            }
        });
        
        if (noResultsMessage) {
            // Show/hide no results message
            if (visibleRows === 0) {
                noResultsMessage.style.display = 'block';
                table.style.display = 'none';
            } else {
                noResultsMessage.style.display = 'none';
                table.style.display = 'table';
            }
        }
    }
    
    // Event listeners for filtering
    searchInput.addEventListener('input', filterTable);

    if (applyFiltersBtn) {
        applyFiltersBtn.addEventListener('click', function() {
            filterTable();
            if (filterDropdown) {
                filterDropdown.style.display = 'none';
            }
        });
    }
    
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', function() {
            searchInput.value = '';
            if (statusFilter)   statusFilter.value   = 'all';
            if (categoryFilter) categoryFilter.value = 'all';
            filterTable();
            if (filterDropdown) filterDropdown.style.display = 'none';
        });
    }

    // ----- Keep your modal code unchanged -----
    function initParticipantModal() { /* ... */ }
    initParticipantModal();

    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                initParticipantModal();
            }
        });
    });
    observer.observe(document.getElementById('studentsTableBody'), {
        childList: true,
        subtree: true
    });
});
