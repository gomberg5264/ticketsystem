document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const createTicketForm = document.getElementById('create-ticket-form');
    const ticketList = document.getElementById('ticket-list');
    const clearTicketsBtn = document.getElementById('clear-tickets-btn');

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    if (createTicketForm) {
        createTicketForm.addEventListener('submit', handleCreateTicket);
    }

    if (ticketList) {
        fetchTickets();
    }

    if (clearTicketsBtn) {
        clearTicketsBtn.addEventListener('click', handleClearTickets);
    }
});

async function handleLogin(e) {
    e.preventDefault();
    const pin = document.getElementById('pin').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pin }),
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('isAdmin', data.is_admin);
            window.location.href = '/tickets';
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function handleCreateTicket(e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const priority = document.getElementById('priority').value;

    try {
        const response = await fetch('/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, description, priority }),
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            fetchTickets(); // Automatically refresh the ticket list
            // Clear the form fields after successful ticket creation
            document.getElementById('title').value = '';
            document.getElementById('description').value = '';
            document.getElementById('priority').value = 'Low';
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchTickets() {
    try {
        const response = await fetch('/tickets');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const tickets = await response.json();
        displayTickets(tickets);
    } catch (error) {
        console.error('Error:', error);
        if (error.message.includes('401')) {
            window.location.href = '/login';
        }
    }
}

function displayTickets(tickets) {
    const ticketList = document.getElementById('ticket-list');
    ticketList.innerHTML = '';

    tickets.forEach(ticket => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${ticket.id}</td>
            <td>${ticket.title}</td>
            <td>${ticket.description}</td>
            <td>${ticket.priority}</td>
            <td>${ticket.status}</td>
            <td>${ticket.created_at}</td>
            <td><button onclick="closeTicket(${ticket.id})">Close</button></td>
        `;
        ticketList.appendChild(row);
    });
}

async function closeTicket(ticketId) {
    try {
        const response = await fetch(`/close_ticket/${ticketId}`, {
            method: 'POST',
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            fetchTickets();
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function handleClearTickets() {
    if (!confirm('Are you sure you want to clear all tickets? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/clear_tickets', {
            method: 'POST',
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            fetchTickets();
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
