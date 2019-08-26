import {Injectable} from '@angular/core';
import {AngularFirestore} from 'angularfire2/firestore';


@Injectable({
  providedIn: 'root'
})
export class FirebaseService {


  constructor(private firestore: AngularFirestore) {
  }

  getInfo() {
    return this.firestore.collection('NGT_Test').valueChanges(); // snapshotChanges() to be able to work on & get ID but more complicated.
  }
}
