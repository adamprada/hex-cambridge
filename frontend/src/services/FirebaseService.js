import firebase from 'firebase';

class FirebaseService {
  signUpTutor = ({ email, password, domains }) => firebase.auth().createUserWithEmailAndPassword(email, password)
      .then(({user}) => firebase.database().ref('users/' + user.uid).set({ uid: user.uid, email, domains }));
  signInTutor = ({ email, password }) => firebase.auth().signInWithEmailAndPassword(email, password);
  signInTutee = () => firebase.auth().signInAnonymously();
  signOut = () => firebase.auth().signOut();
  getTutorData = (uid) => firebase.database().ref('users/' + uid).once('value').then((snapshot) => snapshot.val());
  findMatch = (uid, domain) => firebase.database().ref('users/').once('value').then((snapshot) => {
    const tutors = snapshot.val();
    const availableTutors = Object.values(tutors).filter(u => u.domains.includes(domain)).map(u => u.uid);
    availableTutors.forEach(tutorId => {
      const key = firebase.database().ref('matches/').push().key;
      firebase.database().ref('matches/' + key).set({
        tutorId,
        tuteeId: uid,
        accepted: false,
        jitsiId: key
      })
    })
  });
  uploadFile = (uid, file) => {
    return firebase.storage().ref(uid).put(file).then(() => firebase.storage().ref(uid).getDownloadURL()).then(url => url).catch(err => false);
  }
  getImageUrl = (uid) => {
    return firebase.storage().ref(uid).getDownloadURL().then(url => url);
  }
}

export default new FirebaseService();
