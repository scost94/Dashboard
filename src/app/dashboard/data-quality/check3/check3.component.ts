import {Component, OnInit} from '@angular/core';
import {FirebaseService} from 'src/app/shared/firebase.service';


@Component({
  selector: 'app-check3',
  templateUrl: './check3.component.html',
  styleUrls: ['./check3.component.css']
})

export class Check3Component implements OnInit {

  datasets2: any[] = [];
  public lineChartLabels2: any[];


  newList: any[] = [];
  datasets: any = [];
  data: any;
  boxlabels: any[] = [];


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
      const list = items[0];
      const datavalues: any[] = [];
      const xAxe: any[] = [];
      Object.keys(list).forEach(key1 => {
        xAxe.push(key1);
        datavalues.push(list[key1]);
      });
      this.boxlabels = xAxe;
      // console.log(this.boxlabels)
      this.data = {
        labels: this.boxlabels,
        datasets: [
          {
            label: "Click to hide",
            backgroundColor: "rgba(255,0,0,0.5)",
            borderColor: "red",
            borderWidth: 1,
            outlierColor: "#999999",
            padding: 10,
            itemRadius: 0,
            data: datavalues
          }
        ]
      }


      const list2 = items[1];
      this.lineChartLabels2 = items[1]['Date'];
      this.datasets2 = [{
        label: '1C',
        backgroundColor: 'red',
        borderColor: 'red',
        data: items[1]['1C'],
        fill: false,
      }, {
        label: '1D',
        fill: false,
        backgroundColor: 'blue',
        borderColor: 'blue',
        data: items[1]['1D'],
      },
        {
          label: '2B',
          backgroundColor: 'green',
          borderColor: 'green',
          data: items[1]['2B'],
          fill: false,
        }];

    });
  }
};
