import {Component, OnInit} from '@angular/core';
import {FirebaseService} from 'src/app/shared/firebase.service';

@Component({
  selector: 'app-check2',
  templateUrl: './check2.component.html',
  styleUrls: ['./check2.component.css']
})
export class Check2Component implements OnInit {

  datasets: any[] = [];
  public lineChartLabels: any[];

  public pieChartType: string = 'line';
  public pieChartOptions: any = {
    'backgroundColor': [
      "#FF6384",
      "#4BC0C0",
      "#FFCE56",
      "#E7E9ED",
      "#36A2EB"
    ]
  }

  // events on slice click
  public chartClicked(e: any): void {
    console.log(e);
  }

  // event on line chart slice hover
  public chartHovered(e: any): void {
    console.log(e);
  }


  constructor(private service: FirebaseService) {
  }

  ngOnInit() {
    this.service.getInfo().subscribe((items: any[]) => {
      const list = items[6];
      this.lineChartLabels = items[6]['Date'];
      this.datasets = [{
        label: 'Moving Average',
        backgroundColor: 'red',
        borderColor: 'red',
        data: items[6]['10ma'],
        fill: false,
      }, {
        label: 'NAV_Amount',
        fill: false,
        backgroundColor: 'blue',
        borderColor: 'blue',
        data: items[6]['NAV_Amount'],
      }];
    });
  }
}






