import {Component, ElementRef, OnInit} from '@angular/core';
import {FormGroup, FormControl, FormArray, FormBuilder, Validators} from '@angular/forms'
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-evaluation-form',
  templateUrl: './evaluation-form.component.html',
  styleUrls: ['./evaluation-form.component.css']
})
export class EvaluationFormComponent implements OnInit {

  evaluationForm!:FormGroup;
  keywordSet: any;
  keywords: string[] = [];
  isSubmit: boolean =  false;
  results: any;
  showSpinner: boolean;

  constructor(private formBuilder: FormBuilder,
              private auth: AuthService) { }

  ngOnInit(): void {
    this.evaluationForm = this.formBuilder.group({
      id: ['', [Validators.required]],
      questionNumber: ['', [Validators.required]],
      question: ['', [Validators.required]],
      marks: ['', [Validators.required, Validators.max(100), Validators.min(1)]],
      modelAnswer: ['', [Validators.required]],
      studentAnswer: ['', [Validators.required]],
      keywords: this.keywords
    })
  }

  submit() {
    // enable spinner
    this.auth.setIsShowSpinner(true)
    this.showSpinner = this.auth.getIsShowSpinner()
    this.auth.send_get_request(
      this.evaluationForm.value.id, this.evaluationForm.value.questionNumber, this.evaluationForm.value.question, this.evaluationForm.value.marks,
      this.evaluationForm.value.modelAnswer, this.evaluationForm.value.studentAnswer, this.keywords
    ).subscribe(response => {
      this.auth.setData(response);
      this.results = this.auth.getData();
      // disable spinner
      this.auth.setIsShowSpinner(false)
      this.showSpinner = this.auth.getIsShowSpinner()
      this.isSubmit = true;
    })
  }

  clearForm() {
    this.evaluationForm.reset();
    this.keywords = []
  }

  dropKeyword(index: any) {
    this.keywords.splice(index, 1);
  }

  onKeywordsSetKeydown() {
    if (this.keywordSet == "" || this.keywordSet == null) return;
    if (!this.keywords.includes(this.keywordSet.toLowerCase())) {
      this.keywords.push(this.keywordSet.toLowerCase());
      this.keywordSet = "";}
  }

  scroll(el: HTMLElement) {
    setTimeout(() => {
      el.scrollIntoView(
        {behavior: 'smooth'}
      );
    }, 100);
  }

}

