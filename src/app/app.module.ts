import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AngularFirestoreModule} from 'angularfire2/firestore';
import {AngularFireModule} from 'angularfire2';


import {environment} from '../environments/environment';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {DashboardComponent} from './dashboard/dashboard.component';
import {DataExplorationComponent} from './dashboard/data-exploration/data-exploration.component';
import {DataQualityComponent} from './dashboard/data-quality/data-quality.component';
import {DataVisualizationComponent} from './dashboard/data-visualization/data-visualization.component';
import {ContactComponent} from './contact/contact.component';
import {NotfComponent} from './notf/notf.component';
import {HomeComponent} from './home/home.component';
import {Check3Component} from './dashboard/data-quality/check3/check3.component';
import {Check2Component} from './dashboard/data-quality/check2/check2.component';
import {Check1Component} from './dashboard/data-quality/check1/check1.component';
import {HeatMapAllModule} from '@syncfusion/ej2-angular-heatmap';
import {FirebaseService} from './shared/firebase.service';
import {ChartModule} from "angular2-chartjs";
import {ChartsModule} from 'ng2-charts'
import "chartjs-chart-box-and-violin-plot/build/Chart.BoxPlot.js";


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    DataExplorationComponent,
    DataQualityComponent,
    DataVisualizationComponent,
    ContactComponent,
    NotfComponent,
    HomeComponent,
    Check1Component,
    Check2Component,
    Check3Component,

  ],
  imports: [
    BrowserModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFirestoreModule,
    AppRoutingModule,
    HeatMapAllModule,
    ChartsModule,
    ChartModule
  ],
  providers: [FirebaseService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
