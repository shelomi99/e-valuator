import { Component, OnInit } from '@angular/core';
import {AuthService} from "../services/auth.service";
import {ControlContainer, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-feedback',
  templateUrl: './feedback.component.html',
  styleUrls: ['./feedback.component.css']
})
export class FeedbackComponent implements OnInit {
  evaluationResults: any;
  resultsArray: any;
  evaluationForm: FormGroup;
  feedback: any;


  constructor(private auth: AuthService, private controlContainer: ControlContainer) { }

  ngOnInit(): void {
    // retrieving formGroup values from  evaluation-form component
    this.evaluationForm = <FormGroup>this.controlContainer.control;
    this.evaluationResults = this.auth.getData();
    this.resultsArray = JSON.parse(this.evaluationResults);
    if((this.resultsArray.final_mark/ this.evaluationForm.controls.marks.value) > 0.4){
      this.feedback = 'Good Attempt'
    }else this.feedback = 'Needs Improvement'
  }

  addResult() {
    this.auth.add_result_get_request(
      this.evaluationForm.controls.id.value, this.evaluationForm.controls.questionNumber.value, this.evaluationForm.controls.question.value, this.resultsArray.final_mark,
      this.evaluationForm.controls.marks.value
    ).subscribe(response => {
      console.log(response);
    }, error => {
      console.log("test")
    })
  }

  scrollToTop(){
    window.scroll(0,0);
  }

}
