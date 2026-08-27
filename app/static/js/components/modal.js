// Modal and Drawer helper
window.Modal = {
  open(id) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  },
  close(id) {
    const el = document.getElementById(id);
    if (el) {
      el.classList.remove('active');
      document.body.style.overflow = '';
    }
  },
  toggle(id) {
    const el = document.getElementById(id);
    if (el) {
      if (el.classList.contains('active')) {
        this.close(id);
      } else {
        this.open(id);
      }
    }
  }
};
