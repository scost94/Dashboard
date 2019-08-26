import {Component, OnInit} from '@angular/core';
import {FirebaseService} from 'src/app/shared/firebase.service';

@Component({
  selector: 'app-data-visualization',
  templateUrl: './data-visualization.component.html',
  styleUrls: ['./data-visualization.component.css']
})
export class DataVisualizationComponent implements OnInit {
  newList: any[] = [];
  xAxe: any;

  constructor(private service: FirebaseService) {
  }

  public width: String = '900px';
  public height: String = '500px';

  titleSettings: Object = {
    text: 'Nav_Per_Share Correlation Matrix between The 11 Share Classes',
    textStyle: {
      size: '15px',
      fontWeight: '500',
      fontStyle: 'Normal',
      fontFamily: 'Segoe UI'
    }
  };


  ngOnInit() {
    this.service.getInfo().subscribe((items: any[]) => {
      const list = items[2];
      const list1: any[] = [];
      const xAxe1: any[] = [];
      Object.keys(list).forEach(key1 => {
        xAxe1.push(key1);
        list1.push(list[key1]);
      });
      this.newList = list1;
      this.xAxe = {labels: xAxe1};
    });
  }

}
