let dragging = null;

document.querySelectorAll('.event-card').forEach((card) => {
  card.addEventListener('dragstart', () => {
    dragging = card;
  });
});

document.querySelectorAll('.dropzone').forEach((zone) => {
  zone.addEventListener('dragover', (e) => e.preventDefault());

  zone.addEventListener('drop', async (e) => {
    e.preventDefault();
    if (!dragging) return;

    const column = zone.closest('.column');
    const eventId = dragging.dataset.eventId;
    const status = column.dataset.status;

    const response = await fetch(`/api/events/${eventId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });

    if (response.ok) {
      zone.appendChild(dragging);
    } else {
      alert('Falha ao atualizar status do evento.');
    }
  });
});
