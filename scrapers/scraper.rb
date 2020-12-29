require "HTTParty"
require 'nokogiri'
require 'aws-sdk'

class Poll
    attr_reader :id, :text, :responses

    def initialize(text)
        @id = make_identifier(10)
        @text = text
        @responses = []
    end

    def add_response(text, count)
        response = Response.new(text, count)
        @responses << response
        response
    end

    private 
    
    def make_identifier(length)
        rand(36**length).to_s(36)
    end
end

class Response
    attr_reader :text, :count

    def initialize(text, count)
        @text = text
        @count = count
    end
end

html = HTTParty.get("https://hobbylark.com/party-games/list-of-family-feud-questions")

if not (html.body.nil? || html.body.empty?)
    page = Nokogiri::HTML(html)

    poll_elements = page.css("h2")

    polls = []

    poll_elements[2...].each do |poll_element|
        responses = poll_element.xpath("./following::table[1]//tr")

        next if responses.length == 0

        poll = Poll.new(poll_element.text)

        responses.each do |response_element|
             text = response_element.css('td')[0].text
             responses = response_element.css('td')[1].text.to_i
             response = poll.add_response(text, responses)
        end

        polls << poll
    end

    puts polls.length
    
    dynamodb = Aws::DynamoDB::Client.new(region: 'us-west-2')

    polls.each do |poll|
        item = {
            id: poll.id,
            text: poll.text,
            responses: poll.responses.map do |answer| 
                { text: answer.text, count: answer.count } 
            end
        }
        params = {
            table_name: "polls",
            item: item
        }
        dynamodb.put_item(params)

    end
end