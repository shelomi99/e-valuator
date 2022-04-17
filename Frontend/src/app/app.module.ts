import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { EvaluationFormComponent } from './evaluation-form/evaluation-form.component';
import {NgbAlertModule, NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { FeedbackComponent } from './feedback/feedback.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import { ViewReportComponent } from './view-report/view-report.component';
import {HttpClientModule} from "@angular/common/http";

@NgModule({
  declarations: [
    AppComponent,
    FeedbackComponent,
    EvaluationFormComponent,
    ViewReportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbAlertModule,
    NgbModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]

})
export class AppModule { }
