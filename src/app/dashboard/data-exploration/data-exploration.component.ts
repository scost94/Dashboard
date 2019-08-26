import {Component, OnInit} from '@angular/core';
import {FirebaseService} from 'src/app/shared/firebase.service';

@Component({
  selector: 'app-data-exploration',
  templateUrl: './data-exploration.component.html',
  styleUrls: ['./data-exploration.component.css']
})
export class DataExplorationComponent implements OnInit {

  listOfItems: any;
  listOfItems1: any;
  list: any[] = [];

  row_index: any[] = [];
  first_col: any[] = [];

  constructor(private service: FirebaseService) {
  }

  ngOnInit() {
    // Stats
    this.service.getInfo().subscribe((items: any[]) => {
      this.listOfItems = items[8];
      this.row_index = Object.keys(items[8]);
      this.first_col = Object.keys(items[8][this.row_index[0]]);

      // Descrip
      const listOfKeys: any[] = [];
      this.listOfItems1 = items[3];
      Object.keys(this.listOfItems1).forEach(key => {
        listOfKeys.push(key);
      });
      this.list = listOfKeys;
    });
  }
}
