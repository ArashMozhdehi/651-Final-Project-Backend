function profile_update(message) {
  if (message == "update") {
    toastr.success('Profile updated sucessfully!');
  }
  else if(message == "not_same") {
    toastr.error('Entered passwords are not the same! Please make sure the use the same word for both.');
  }
}
