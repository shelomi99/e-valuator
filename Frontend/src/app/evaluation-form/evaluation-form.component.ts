import {Component, ElementRef, OnInit, ViewChild} from '@angular/core';
import {FormGroup, FormControl, FormArray, FormBuilder, Validators} from '@angular/forms'
import {AuthService} from "../services/auth.service";

@Component({
  selector: 'app-evaluation-form',
  templateUrl: './evaluation-form.component.html',
  styleUrls: ['./evaluation-form.component.css']
})
export class EvaluationFormComponent implements OnInit {
  @ViewChild('inputKeywords') inputKeyword;
  evaluationForm!:FormGroup;
  keywordSet: any;
  keywords: string[] = [];
  isSubmit: boolean =  false;
  results: any;
  showSpinner: boolean;
  disable : boolean;
  isError : any;

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
    this.isError = false;
    this.disable = false;
    // enable spinner
    this.auth.setIsShowSpinner(true)
    this.showSpinner = this.auth.getIsShowSpinner()
    this.auth.send_get_request(
      this.evaluationForm.value.id, this.evaluationForm.value.questionNumber, this.evaluationForm.value.question, this.evaluationForm.value.marks,
      this.evaluationForm.value.modelAnswer, this.evaluationForm.value.studentAnswer, this.keywords
    ).subscribe(response => {
      this.disable = true;
      this.auth.setData(response);
      this.results = this.auth.getData();
      // disable spinner
      this.auth.setIsShowSpinner(false);
      this.showSpinner = this.auth.getIsShowSpinner();
      this.isSubmit = true;
    }, (error => {
      this.showSpinner = false;
      this.isError = true;
    }))
  }

  clearForm() {
    this.evaluationForm.reset();
    this.keywords = []
  }

  dropKeyword(index: any) {
    this.keywords.splice(index, 1);
  }

  onKeywordsSetKeydown() {
    if (this.evaluationForm.value.keywords == " " || this.evaluationForm.value.keywords == "" || this.evaluationForm.value.keywords == null) return;
    if (!this.keywords.includes(this.evaluationForm.value.keywords.toLowerCase())) {
      this.keywords.push(this.evaluationForm.value.keywords.toLowerCase());
      this.evaluationForm.value.keywords = "";
      this.inputKeyword.nativeElement.value = '';
    }
  }

  scroll(el: HTMLElement) {
    setTimeout(() => {
      el.scrollIntoView(
        {behavior: 'smooth'}
      );
    }, 100);
  }

}

