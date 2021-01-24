import React from 'react';
import './App.css';
import firebase from 'firebase';
import { FirebaseAuthProvider, FirebaseAuthConsumer, IfFirebaseAuthed, IfFirebaseUnAuthed } from '@react-firebase/auth';
import { FirebaseDatabaseProvider } from '@react-firebase/database';

// Screens
import Landing from './screens/Landing';
import Tutee from './screens/Tutee/Tutee';
import Tutor from './screens/Tutor/Tutor';

export default function App() {
  return (
    <FirebaseAuthProvider firebase={firebase}>
      <FirebaseDatabaseProvider firebase={firebase}>
        <IfFirebaseUnAuthed>
          <Landing />
        </IfFirebaseUnAuthed>
        <IfFirebaseAuthed>
          <FirebaseAuthConsumer>
            {({ isSignedIn, user, providerId }) => {
              if (user.email) {
                return <Tutor uid={user.uid} />
              }
              return <Tutee uid={user.uid} />
            }}
          </FirebaseAuthConsumer>
        </IfFirebaseAuthed>
      </FirebaseDatabaseProvider>
    </FirebaseAuthProvider>
  );
}