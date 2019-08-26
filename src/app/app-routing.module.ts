import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {DashboardComponent} from './dashboard/dashboard.component';
import {DataExplorationComponent} from './dashboard/data-exploration/data-exploration.component';
import {DataQualityComponent} from './dashboard/data-quality/data-quality.component';
import {DataVisualizationComponent} from './dashboard/data-visualization/data-visualization.component';
import {ContactComponent} from './contact/contact.component';
import {NotfComponent} from './notf/notf.component';
import {HomeComponent} from './home/home.component';
import {Check1Component} from './dashboard/data-quality/check1/check1.component';
import {Check2Component} from './dashboard/data-quality/check2/check2.component';
import {Check3Component} from './dashboard/data-quality/check3/check3.component';


const routes: Routes = [
  {
    path: "dashboard", component: DashboardComponent, children: [
      {path: "exploration", component: DataExplorationComponent},
      {
        path: "quality", component: DataQualityComponent, children:
          [
            {path: "check1", component: Check1Component},
            {path: "check2", component: Check2Component},
            {path: "check3", component: Check3Component}
          ]

      },
      {path: "visualization", component: DataVisualizationComponent}
    ]
  },
  {
    path: "contact", component: ContactComponent
  },
  {
    path: "", component: HomeComponent
  },
  {
    path: "**", component: NotfComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
