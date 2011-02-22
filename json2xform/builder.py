from survey_element import SurveyElement
from question import Question, InputQuestion, UploadQuestion, MultipleChoiceQuestion
from section import Section
from survey import Survey
import utils

class SurveyElementBuilder(object):
    # we use this CLASSES dict to create questions from dictionaries
    QUESTION_CLASSES = {
        u"" : Question,
        u"input" : InputQuestion,
        u"select" : MultipleChoiceQuestion,
        u"select1" : MultipleChoiceQuestion,
        u"upload" : UploadQuestion,
        }

    SECTION_CLASSES = {
        u"group" : Section,
        u"survey" : Survey,
        }

    def _get_question_class(self, question_type_str):
        question_type = Question.TYPES[question_type_str]
        control_dict = question_type[Question.CONTROL]
        control_tag = control_dict.get(u"tag", u"")
        return self.QUESTION_CLASSES[control_tag]

    def _create_question_from_dict(self, d):
        question_type_str = d[Question.TYPE]
        if question_type_str.endswith(u" or specify other"):
            question_type_str = question_type_str[:len(question_type_str)-len(u" or specify other")]
        question_class = self._get_question_class(question_type_str)
        return question_class(**d)

    def _create_section_from_dict(self, d):
        # this messes with the dictionary, might want to avoid this side effect
        children = d.pop(Section.CHILDREN)
        section_class = self.SECTION_CLASSES[d[Section.TYPE]]
        result = section_class(**d)
        for child in children:
            survey_element = self.create_survey_element_from_dict(child)
            result.add_child(survey_element)
        return result

    def create_survey_element_from_dict(self, d):
        if d[SurveyElement.TYPE] in self.SECTION_CLASSES:
            return self._create_section_from_dict(d)
        else:
            return self._create_question_from_dict(d)

def create_survey_element_from_dict(d):
    builder = SurveyElementBuilder()
    return builder.create_survey_element_from_dict(d)

def create_survey_element_from_json(str_or_path):
    d = utils.get_pyobj_from_json(str_or_path)
    return create_survey_element_from_dict(d)

# we will need to write a helper function to create tables of questions
# i'm thinking the excel syntax will look something like:
# begin table with columns from ...
# row1
# row2 ...
# end table
# def table(rows, columns):
#     result = []
#     for row_text, row_name in tuples(rows):
#         for d in columns:
#             kwargs = d.copy()
#             kwargs["text"] = row_text + u": " + kwargs["text"]
#             kwargs["name"] = row_name + u" " + kwargs.get("name", sluggify(kwargs["text"]))
#             result.append(q(**kwargs))
#     return result