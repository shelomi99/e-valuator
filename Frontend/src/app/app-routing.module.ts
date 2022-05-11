import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {EvaluationFormComponent} from "./evaluation-form/evaluation-form.component";
import {FeedbackComponent} from "./feedback/feedback.component";
import {ViewReportComponent} from "./view-report/view-report.component";

const routes: Routes = [
  {
    path: '',
    component: EvaluationFormComponent
  },
  {
    path: 'feedback',
    component: FeedbackComponent
  },
  {
    path: 'report',
    component: ViewReportComponent
  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
