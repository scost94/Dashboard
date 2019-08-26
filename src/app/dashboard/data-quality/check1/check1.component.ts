import {Component, OnInit} from '@angular/core';
import {FirebaseService} from 'src/app/shared/firebase.service';

@Component({
  selector: 'app-check1',
  templateUrl: './check1.component.html',
  styleUrls: ['./check1.component.css']
})
export class Check1Component implements OnInit {
  msg1: any;
  value1: any;

  msg2: any;
  value2: any;


  barchartdata: any[] = [];
  barchartlabels: any;


  public barcharttype = 'bar';
  public barchartlegend = false;


  constructor(private service: FirebaseService) {
  }

  public barchartoptions = {
    scaleShowVerticalLines: false,
    responsive: true
  };


  ngOnInit() {
    this.service.getInfo().subscribe((items: any[]) => {
      //console.log('items', items);

      // Missing values
      Object.keys(items[5]).forEach(key => {
        this.msg1 = key;
        this.value1 = items[5][key];
      });


      // // Missing dates
      const list2 = items[4];
      const labels1: any[] = [];
      const ouput: any[] = [];
      Object.keys(list2).forEach(key2 => {
        labels1.push(key2);
        ouput.push({"data": list2[key2], "label": key2})
      });

      // Duplicated data
      Object.keys(items[7]).forEach(key => {
        this.msg2 = key;
        this.value2 = items[7][key];
      });


      this.barchartdata = ouput;
      this.barchartlabels = labels1;
    });
  }
}


